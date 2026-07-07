import argparse
import base64
from dataclasses import dataclass
import json
import math
from pathlib import Path
import re
import time
from typing import Dict, Iterable, List, Optional, Tuple
import html

import pandas as pd
import requests


@dataclass(frozen=True)
class PrepConfig:
    output_dir: Path
    symbol: str
    adjust_mode: str
    date_col: str
    tz: str


def _norm_symbol(sym: str) -> str:
    s = (sym or "").strip().upper()
    if not s:
        return s
    if s.endswith(".SH") or s.endswith(".SZ") or s.endswith(".BJ"):
        return s
    if s.startswith("6"):
        return f"{s}.SH"
    if s.startswith(("0", "3")):
        return f"{s}.SZ"
    if s.startswith(("8", "4")):
        return f"{s}.BJ"
    return s


def _to_ticker(code6: str) -> str:
    c = _coerce_code6(code6)
    if not c:
        return ""
    ex = _infer_exchange(c)
    if not ex:
        return c
    return f"{c}.{ex}"


def _board_tag(code6: str) -> str:
    c = _coerce_code6(code6)
    if not c:
        return ""
    if c.startswith(("688", "689")):
        return "STAR"
    if c.startswith(("300", "301")):
        return "CYB"
    if c.startswith(("000", "001", "002", "003")):
        return "SZ_MAIN"
    if c.startswith(("600", "601", "603", "605")):
        return "SH_MAIN"
    if c.startswith(("8", "4")):
        return "BJ"
    if c.startswith(("200", "201", "900")):
        return "B_SHARE"
    return "OTHER"


def _is_cn_retail_tradable(code6: str) -> bool:
    return _board_tag(code6) in {"SH_MAIN", "SZ_MAIN", "CYB"}


def _first_existing(cols: Iterable[str], candidates: Iterable[str]) -> Optional[str]:
    cols_u = {c.strip(): c for c in cols}
    for cand in candidates:
        if cand in cols_u:
            return cols_u[cand]
    return None


def _parse_date_series(s: pd.Series) -> pd.Series:
    if s.dtype == "datetime64[ns]" or str(s.dtype).startswith("datetime64"):
        return s
    if s.dtype == "int64" or s.dtype == "int32":
        return pd.to_datetime(s.astype(str), format="%Y%m%d", errors="coerce")
    if s.dtype == "object":
        ss = s.astype(str).str.strip()
        dt = pd.to_datetime(ss, errors="coerce")
        if dt.isna().mean() > 0.5:
            dt2 = pd.to_datetime(ss, format="%Y%m%d", errors="coerce")
            if dt2.isna().mean() < dt.isna().mean():
                return dt2
        return dt
    return pd.to_datetime(s, errors="coerce")


def _detect_columns(df: pd.DataFrame, date_col_hint: Optional[str]) -> Dict[str, str]:
    cols = list(df.columns)
    out: Dict[str, str] = {}
    if date_col_hint and date_col_hint in df.columns:
        out["date"] = date_col_hint
    else:
        out["date"] = _first_existing(cols, ["date", "datetime", "time", "trade_date", "交易日期", "日期"]) or ""
    out["open"] = _first_existing(cols, ["open", "Open", "开盘", "开盘价"]) or ""
    out["high"] = _first_existing(cols, ["high", "High", "最高", "最高价"]) or ""
    out["low"] = _first_existing(cols, ["low", "Low", "最低", "最低价"]) or ""
    out["close"] = _first_existing(cols, ["close", "Close", "收盘", "收盘价"]) or ""
    out["volume"] = _first_existing(cols, ["vol", "volume", "Volume", "成交量"]) or ""
    out["amount"] = _first_existing(cols, ["amount", "成交额", "turnover"]) or ""
    out["adj_factor"] = _first_existing(cols, ["adj_factor", "adj", "复权因子", "factor"]) or ""
    out["symbol"] = _first_existing(cols, ["ts_code", "symbol", "code", "代码", "证券代码"]) or ""
    return out


def _ensure_required(cols_map: Dict[str, str]) -> None:
    missing = [k for k in ["date", "open", "high", "low", "close"] if not cols_map.get(k)]
    if missing:
        raise ValueError(f"missing required columns: {missing}")


def _apply_adjust(df: pd.DataFrame, mode: str) -> pd.DataFrame:
    m = (mode or "none").strip().lower()
    if m == "none":
        return df
    if "adj_factor" not in df.columns:
        raise ValueError("adjust_mode requires adj_factor column")
    f = pd.to_numeric(df["adj_factor"], errors="coerce")
    if f.isna().any():
        raise ValueError("adj_factor has NaN values")
    if m not in {"qfq", "hfq"}:
        raise ValueError("adjust_mode must be one of: none,qfq,hfq")
    if m == "qfq":
        base = float(f.iloc[-1])
        scale = f / base
    else:
        base = float(f.iloc[0])
        scale = f / base
    for c in ["open", "high", "low", "close"]:
        df[f"{c}_{m}"] = pd.to_numeric(df[c], errors="coerce") * scale
    return df


def _validate(df: pd.DataFrame) -> List[str]:
    issues: List[str] = []
    if df["date"].isna().any():
        issues.append("date has NaN after parsing")
    if df["date"].duplicated().any():
        issues.append("date has duplicates")
    for c in ["open", "high", "low", "close"]:
        s = pd.to_numeric(df[c], errors="coerce")
        if s.isna().any():
            issues.append(f"{c} has NaN")
        if (s <= 0).any():
            issues.append(f"{c} has non-positive values")
    if "volume" in df.columns:
        v = pd.to_numeric(df["volume"], errors="coerce")
        if (v < 0).any():
            issues.append("volume has negative values")
    if "amount" in df.columns:
        a = pd.to_numeric(df["amount"], errors="coerce")
        if (a < 0).any():
            issues.append("amount has negative values")
    if (pd.to_numeric(df["high"], errors="coerce") < pd.to_numeric(df["low"], errors="coerce")).any():
        issues.append("high < low exists")
    return issues


def preprocess_one(cfg: PrepConfig, df0: pd.DataFrame) -> Tuple[Path, pd.DataFrame]:
    cfg.output_dir.mkdir(parents=True, exist_ok=True)
    cols_map = _detect_columns(df0, cfg.date_col)
    _ensure_required(cols_map)

    df = pd.DataFrame()
    df["date"] = _parse_date_series(df0[cols_map["date"]])
    df["open"] = df0[cols_map["open"]]
    df["high"] = df0[cols_map["high"]]
    df["low"] = df0[cols_map["low"]]
    df["close"] = df0[cols_map["close"]]

    if cols_map.get("volume"):
        df["volume"] = df0[cols_map["volume"]]
    if cols_map.get("amount"):
        df["amount"] = df0[cols_map["amount"]]
    if cols_map.get("adj_factor"):
        df["adj_factor"] = df0[cols_map["adj_factor"]]

    sym = _norm_symbol(cfg.symbol)
    if not sym and cols_map.get("symbol"):
        s = str(df0[cols_map["symbol"]].iloc[0])
        sym = _norm_symbol(s)
    df["symbol"] = sym

    df = df.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    df = _apply_adjust(df, cfg.adjust_mode)

    issues = _validate(df)
    if issues:
        raise ValueError(" | ".join(issues))

    out_path = cfg.output_dir / f"{sym.replace('.', '_')}_1d.csv"
    df.to_csv(out_path, index=False)
    return out_path, df


def _fetch_akshare_1d(symbol_6: str, start: str, end: str, adjust: str) -> pd.DataFrame:
    try:
        import akshare as ak  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "akshare is not available. Install it in your venv first: pip install akshare"
        ) from e

    sym = (symbol_6 or "").strip()
    if not sym.isdigit() or len(sym) != 6:
        raise ValueError("akshare fetch requires a 6-digit A-share code like 300750")
    s = (start or "").strip()
    e = (end or "").strip()
    if not s:
        s = "20100101"
    if not e:
        e = "20991231"
    adj = (adjust or "none").strip().lower()
    ak_adj = "" if adj == "none" else adj
    last_err: Optional[Exception] = None
    for attempt in range(1, 11):
        try:
            df = ak.stock_zh_a_hist(
                symbol=sym,
                period="daily",
                start_date=s,
                end_date=e,
                adjust=ak_adj,
                timeout=30,
            )
            if df is None or len(df) == 0:
                raise ValueError("akshare returned empty dataframe")
            return df
        except Exception as ex:
            last_err = ex
            time.sleep(min(2 * attempt, 20))
    raise RuntimeError(f"akshare fetch failed after retries: {last_err}") from last_err


def _to_baostock_code(symbol_6: str) -> str:
    s = (symbol_6 or "").strip()
    if not s.isdigit() or len(s) != 6:
        raise ValueError("baostock fetch requires a 6-digit A-share code like 300750")
    if s.startswith("6"):
        return f"sh.{s}"
    if s.startswith(("0", "3")):
        return f"sz.{s}"
    if s.startswith(("8", "4")):
        return f"bj.{s}"
    return f"sz.{s}"


def _fetch_baostock_1d(symbol_6: str, start: str, end: str, adjust: str) -> pd.DataFrame:
    try:
        import baostock as bs  # type: ignore
    except Exception as e:
        raise RuntimeError(
            "baostock is not available. Install it in your venv first: pip install baostock"
        ) from e

    lg = bs.login()
    if getattr(lg, "error_code", "0") != "0":
        raise RuntimeError(f"baostock login failed: {getattr(lg,'error_msg','')}")
    try:
        return _fetch_baostock_1d_with_session(bs, symbol_6=symbol_6, start=start, end=end, adjust=adjust)
    finally:
        bs.logout()


def _fetch_baostock_1d_with_session(bs: object, symbol_6: str, start: str, end: str, adjust: str) -> pd.DataFrame:
    code = _to_baostock_code(symbol_6)
    s = (start or "").strip()
    e = (end or "").strip()
    if not s:
        s = "2010-01-01"
    if not e:
        e = "2099-12-31"

    adj = (adjust or "none").strip().lower()
    if adj == "none":
        adj_flag = "3"
    elif adj == "qfq":
        adj_flag = "2"
    elif adj == "hfq":
        adj_flag = "1"
    else:
        raise ValueError("adjust must be one of: none,qfq,hfq")

    rs = bs.query_history_k_data_plus(
        code,
        "date,code,open,high,low,close,volume,amount,adjustflag",
        start_date=s,
        end_date=e,
        frequency="d",
        adjustflag=adj_flag,
    )
    if getattr(rs, "error_code", "0") != "0":
        raise RuntimeError(f"baostock query failed: {getattr(rs,'error_msg','')}")
    rows: List[List[str]] = []
    while rs.next():
        rows.append(rs.get_row_data())
    if not rows:
        raise ValueError("baostock returned empty rows")
    df0 = pd.DataFrame(
        rows,
        columns=["date", "code", "open", "high", "low", "close", "volume", "amount", "adjustflag"],
    )
    df0["date"] = pd.to_datetime(df0["date"], errors="coerce")
    for c in ["open", "high", "low", "close", "volume", "amount"]:
        df0[c] = pd.to_numeric(df0[c], errors="coerce")
    df0 = df0.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    df0["symbol"] = _norm_symbol(symbol_6)
    return df0.rename(columns={"code": "ts_code"})


def _load_input_df(args: argparse.Namespace) -> Tuple[pd.DataFrame, str]:
    fetch = str(getattr(args, "fetch", "none") or "none").strip().lower()
    if getattr(args, "input", None):
        return pd.read_csv(Path(str(args.input))), "csv"
    if fetch == "akshare":
        df0 = _fetch_akshare_1d(
            symbol_6=str(args.symbol or ""),
            start=str(args.start_date or ""),
            end=str(args.end_date or ""),
            adjust=str(args.adjust or "none"),
        )
        return df0, "akshare"
    if fetch == "baostock":
        df0 = _fetch_baostock_1d(
            symbol_6=str(args.symbol or ""),
            start=str(args.start_date or ""),
            end=str(args.end_date or ""),
            adjust=str(args.adjust or "none"),
        )
        return df0, "baostock"
    raise ValueError("either --input must be provided, or set --fetch akshare with --symbol")


def _http_get(url: str, timeout_s: int = 20, retries: int = 5) -> bytes:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.7",
        "Connection": "close",
    }
    last_err: Optional[Exception] = None
    for attempt in range(1, max(1, retries) + 1):
        try:
            resp = requests.get(url, headers=headers, timeout=timeout_s)
            resp.raise_for_status()
            return resp.content
        except Exception as e:
            last_err = e
            time.sleep(min(2 * attempt, 10))
    raise RuntimeError(f"http get failed after retries: {last_err}") from last_err


def _fetch_quicktiny_ladder() -> Dict[str, object]:
    url = "https://stock.quicktiny.cn/api/ladder"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "application/json,text/plain,*/*",
        "Referer": "https://stock.quicktiny.cn/stock-ladder",
        "Connection": "close",
    }
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    if not isinstance(data, dict):
        raise ValueError("quicktiny ladder api returned non-dict json")
    return data


def ladder_healthcheck_quicktiny(n: int = 10) -> Dict[str, object]:
    n = int(n) if int(n) > 0 else 10
    need_stock_fields = ["code", "name", "continue_num", "tags", "open_num"]
    latencies: List[float] = []
    ok_runs = 0
    missing_runs = 0
    last_missing: List[str] = []
    last_stock_keys: List[str] = []

    for _ in range(n):
        t0 = time.time()
        data = _fetch_quicktiny_ladder()
        latencies.append(float(time.time() - t0))

        dates = data.get("dates", [])
        if not isinstance(dates, list) or not dates or not isinstance(dates[0], dict):
            missing_runs += 1
            last_missing = ["dates"]
            continue
        d0 = dates[0]
        boards = d0.get("boards", [])
        if not isinstance(boards, list) or not boards:
            missing_runs += 1
            last_missing = ["boards"]
            continue
        stocks: List[Dict[str, object]] = []
        for b in boards:
            if not isinstance(b, dict):
                continue
            ss = b.get("stocks", [])
            if isinstance(ss, list):
                stocks.extend([x for x in ss if isinstance(x, dict)])
        if not stocks:
            missing_runs += 1
            last_missing = ["stocks"]
            continue
        s0 = stocks[0]
        last_stock_keys = list(s0.keys())
        missing = [k for k in need_stock_fields if k not in s0]
        if missing:
            missing_runs += 1
            last_missing = missing
        else:
            ok_runs += 1

    lat_sorted = sorted(latencies)
    p50 = lat_sorted[len(lat_sorted) // 2] if lat_sorted else 0.0
    p95 = lat_sorted[max(int(len(lat_sorted) * 0.95) - 1, 0)] if lat_sorted else 0.0
    mx = max(lat_sorted) if lat_sorted else 0.0
    return {
        "n": n,
        "ok_runs": ok_runs,
        "missing_runs": missing_runs,
        "p50_s": p50,
        "p95_s": p95,
        "max_s": mx,
        "last_missing": last_missing,
        "sample_stock_keys": last_stock_keys,
    }


def _ollama_generate(
    ollama_url: str,
    model: str,
    prompt: str,
    images_b64: Optional[List[str]] = None,
    timeout_s: int = 120,
) -> str:
    base = (ollama_url or "").strip().rstrip("/")
    if not base:
        base = "http://localhost:11434"
    if images_b64:
        url = f"{base}/api/chat"
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt, "images": images_b64}],
            "stream": False,
        }
    else:
        url = f"{base}/api/generate"
        payload = {"model": model, "prompt": prompt, "stream": False}
    resp = requests.post(url, json=payload, timeout=int(timeout_s))
    resp.raise_for_status()
    j = resp.json()
    if not isinstance(j, dict):
        raise ValueError("ollama api returned non-dict json")
    if "message" in j and isinstance(j.get("message"), dict):
        return str(j["message"].get("content", "") or "")
    return str(j.get("response", "") or "")


def _extract_json_from_text(s: str) -> Dict[str, object]:
    ss = (s or "").strip()
    if not ss:
        return {}
    ss = re.sub(r"^```(?:json)?\s*", "", ss, flags=re.I)
    ss = re.sub(r"\s*```$", "", ss, flags=re.I)
    b = ss.find("{")
    e = ss.rfind("}")
    if b >= 0 and e > b:
        ss = ss[b : e + 1]
    return json.loads(ss)


def blogroom_summarize_with_ollama(
    blogroom_dir: Path,
    out_dir: Path,
    out_tag: str,
    ollama_url: str,
    ollama_model: str,
    logic_model: str,
    ocr_mode: str,
    max_images: int,
    timeout_s: int,
) -> Tuple[Path, Path]:
    blogroom_dir = Path(blogroom_dir)
    if not blogroom_dir.exists() or not blogroom_dir.is_dir():
        raise ValueError(f"blogroom_dir not found: {blogroom_dir}")

    exts = {".png", ".jpg", ".jpeg", ".webp"}
    imgs = [p for p in blogroom_dir.iterdir() if p.is_file() and p.suffix.lower() in exts]
    if not imgs:
        raise ValueError(f"no images found in blogroom_dir: {blogroom_dir}")
    imgs.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    imgs = imgs[: max(int(max_images), 1)]

    tag = str(out_tag or "").strip() or time.strftime("%Y%m%d")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_jsonl = out_dir / f"blogroom_summary_{tag}.jsonl"
    out_codes = out_dir / f"blogroom_codes_{tag}.csv"

    summary_rows: List[Dict[str, object]] = []
    all_codes: Dict[str, int] = {}

    vision_prompt = (
        "请尽可能原样转写图片中的文字，重点保留：6位数字、股票简称/别名/缩写、题材/行业关键词。\n"
        "不要总结，不要改写。\n"
        "若出现个人隐私信息（姓名/手机号/账号/地址等），用[REDACTED]替代。\n"
        "只输出转写文本。"
    )

    logic_prompt_tpl = (
        "你是一名严谨的信息抽取助手。给你一段直播间转写文本，请抽取结构化信息，只输出JSON对象，不要输出任何解释文字。\n"
        "要求：\n"
        "1) codes 只能包含文本中明确出现的6位数字股票代码（不要猜）。\n"
        "2) names 提取文本中出现的股票名称/简称/谐音/缩写（原样保留）。\n"
        "3) topics 提取出现的题材/行业关键词（原样保留）。\n"
        "4) 若无法确定 time/speaker 可留空字符串。\n"
        "输出JSON格式：\n"
        '{ "time": "", "speaker": "", "codes": [], "names": [], "topics": [] }'
    )

    mode = str(ocr_mode or "").strip().lower() or "ollama"
    easy_reader = None
    easy_gpu = False
    if mode == "easyocr":
        try:
            import easyocr  # type: ignore
        except Exception as e:
            raise RuntimeError("easyocr not installed; run: .\\.venv\\Scripts\\python.exe -m pip install easyocr") from e
        try:
            import torch  # type: ignore

            easy_gpu = bool(torch.cuda.is_available())
        except Exception:
            easy_gpu = False
        easy_reader = easyocr.Reader(["ch_sim", "en"], gpu=easy_gpu)

    for i, p in enumerate(imgs, start=1):
        print(f"[A_SHARE_PREP] blogroom {i}/{len(imgs)} image={p.name}")
        text = ""
        if mode == "easyocr":
            try:
                import numpy as np  # type: ignore
                from PIL import Image  # type: ignore

                img = Image.open(p).convert("RGB")
                img_arr = np.array(img)
                rows = easy_reader.readtext(img_arr, detail=0, paragraph=True) if easy_reader else []
                if isinstance(rows, list):
                    text = "\n".join([str(x) for x in rows if str(x).strip()]).strip()
            except Exception as e:
                raise RuntimeError(f"easyocr failed on image: {p}") from e
        else:
            b = p.read_bytes()
            b64 = base64.b64encode(b).decode("utf-8")
            resp_text = ""
            for attempt in range(1, 3):
                try:
                    resp_text = _ollama_generate(
                        ollama_url=ollama_url,
                        model=ollama_model,
                        prompt=vision_prompt,
                        images_b64=[b64],
                        timeout_s=timeout_s,
                    )
                    break
                except requests.exceptions.ReadTimeout:
                    if attempt >= 2:
                        raise
                    time.sleep(2.0)
            text = str(resp_text or "").strip()
        codes = sorted(set(re.findall(r"(?<!\d)(\d{6})(?!\d)", text)))
        obj: Dict[str, object] = {
            "source_image": str(p.name),
            "time": "",
            "speaker": "",
            "text": text,
            "codes": codes,
            "names": [],
            "topics": [],
        }

        lm = str(logic_model or "").strip()
        if lm and lm.lower() not in {"none", "off", "false", "0"} and text:
            resp2 = _ollama_generate(
                ollama_url=ollama_url,
                model=lm,
                prompt=logic_prompt_tpl + "\n\n转写文本：\n" + text,
                images_b64=None,
                timeout_s=timeout_s,
            )
            try:
                obj2 = _extract_json_from_text(resp2)
                if isinstance(obj2, dict):
                    for k in ["time", "speaker", "names", "topics", "codes"]:
                        if k in obj2:
                            obj[k] = obj2[k]
                    if isinstance(obj.get("codes"), list):
                        obj["codes"] = [str(x) for x in obj["codes"]]
            except Exception:
                pass

        summary_rows.append(obj)

        codes = obj.get("codes", [])
        if isinstance(codes, list):
            for c in codes:
                c6 = _coerce_code6(str(c))
                if not c6 or not _is_cn_retail_tradable(c6):
                    continue
                all_codes[c6] = int(all_codes.get(c6, 0)) + 1

    out_jsonl.write_text("\n".join([json.dumps(x, ensure_ascii=False) for x in summary_rows]) + "\n", encoding="utf-8")

    if all_codes:
        df = pd.DataFrame([{"code": k, "ticker": _to_ticker(k), "blog_count": v} for k, v in all_codes.items()])
        df = df.sort_values(["blog_count", "code"], ascending=[False, True]).reset_index(drop=True)
        mx = int(df["blog_count"].max() or 1)
        df["blog_score"] = df["blog_count"].map(lambda x: float((math.log1p(int(x)) / math.log1p(mx))) if mx > 0 else 0.0)
        df.to_csv(out_codes, index=False, encoding="utf-8-sig")
    else:
        pd.DataFrame(columns=["code", "ticker", "blog_count", "blog_score"]).to_csv(out_codes, index=False, encoding="utf-8-sig")

    return out_jsonl, out_codes


def blogroom_aggregate_jsonl(
    summary_jsonl: Path,
    out_dir: Path,
    out_tag: str,
    min_count: int = 1,
) -> Tuple[Path, Path]:
    summary_jsonl = Path(summary_jsonl)
    if not summary_jsonl.exists() or not summary_jsonl.is_file():
        raise ValueError(f"summary_jsonl not found: {summary_jsonl}")

    tag = str(out_tag or "").strip()
    if not tag:
        m = re.search(r"blogroom_summary_(.+)\.jsonl$", summary_jsonl.name)
        tag = m.group(1) if m else time.strftime("%Y%m%d")

    out_dir.mkdir(parents=True, exist_ok=True)
    out_topics = out_dir / f"blogroom_topics_{tag}.csv"
    out_names = out_dir / f"blogroom_names_{tag}.csv"

    topic_cnt: Dict[str, int] = {}
    name_cnt: Dict[str, int] = {}

    with summary_jsonl.open("r", encoding="utf-8") as f:
        for line in f:
            line = (line or "").strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            if not isinstance(obj, dict):
                continue
            topics = obj.get("topics", [])
            names = obj.get("names", [])
            if (not topics or not names) and isinstance(obj.get("text"), str) and obj.get("text"):
                txt = str(obj.get("text") or "")
                try:
                    obj2 = json.loads(txt)
                    if isinstance(obj2, dict):
                        if not topics and isinstance(obj2.get("topics"), list):
                            topics = obj2.get("topics", [])
                        if not names and isinstance(obj2.get("names"), list):
                            names = obj2.get("names", [])
                except Exception:
                    pass
            if isinstance(topics, list):
                for t in topics:
                    s = str(t or "").strip()
                    if not s:
                        continue
                    topic_cnt[s] = int(topic_cnt.get(s, 0)) + 1
            if isinstance(names, list):
                for n in names:
                    s = str(n or "").strip()
                    if not s:
                        continue
                    name_cnt[s] = int(name_cnt.get(s, 0)) + 1

    def _to_df(d: Dict[str, int], col: str) -> pd.DataFrame:
        rows = [{"item": k, "count": int(v)} for k, v in d.items() if int(v) >= int(min_count)]
        if not rows:
            return pd.DataFrame(columns=[col, "count"])
        df = pd.DataFrame(rows).sort_values(["count", "item"], ascending=[False, True]).reset_index(drop=True)
        df = df.rename(columns={"item": col})
        return df

    _to_df(topic_cnt, "topic").to_csv(out_topics, index=False, encoding="utf-8-sig")
    _to_df(name_cnt, "name").to_csv(out_names, index=False, encoding="utf-8-sig")
    return out_topics, out_names


def _har_entries(har: Dict[str, object]) -> List[Dict[str, object]]:
    log = har.get("log", {}) if isinstance(har, dict) else {}
    if not isinstance(log, dict):
        return []
    ent = log.get("entries", [])
    return ent if isinstance(ent, list) else []


def _har_get_response_text(entry: Dict[str, object]) -> Tuple[str, str, int, str]:
    req = entry.get("request", {}) if isinstance(entry, dict) else {}
    resp = entry.get("response", {}) if isinstance(entry, dict) else {}
    url = str(req.get("url", "") or "") if isinstance(req, dict) else ""
    status = int(resp.get("status", 0) or 0) if isinstance(resp, dict) else 0
    content = resp.get("content", {}) if isinstance(resp, dict) else {}
    mime = str(content.get("mimeType", "") or "") if isinstance(content, dict) else ""
    text = str(content.get("text", "") or "") if isinstance(content, dict) else ""
    enc = str(content.get("encoding", "") or "") if isinstance(content, dict) else ""
    if enc == "base64" and text:
        try:
            text = base64.b64decode(text).decode("utf-8", errors="replace")
        except Exception:
            pass
    return url, mime, status, text


def mx2025_extract_from_har(
    har_path: Path,
    out_dir: Path,
    out_tag: str,
    ollama_url: str,
    logic_model: str,
    timeout_s: int,
    url_contains: str = "",
) -> Path:
    har_path = Path(har_path)
    if not har_path.exists() or not har_path.is_file():
        raise ValueError(f"har_path not found: {har_path}")

    out_dir.mkdir(parents=True, exist_ok=True)
    tag = str(out_tag or "").strip() or time.strftime("%Y%m%d")
    out_jsonl = out_dir / f"mx2025_summary_{tag}.jsonl"

    har = json.loads(har_path.read_text(encoding="utf-8"))
    entries = _har_entries(har)
    if not entries:
        raise ValueError("HAR has no entries")

    has_body = 0
    for e in entries:
        if not isinstance(e, dict):
            continue
        _, _, _, t = _har_get_response_text(e)
        if t:
            has_body += 1
            break
    if has_body == 0:
        raise ValueError(
            "HAR 不包含响应正文（content.text 全为空）。你导出的很可能是“已清理/脱敏”的 HAR。\n"
            "请在 Network 面板使用“Export HAR / Save all as HAR with content（包含内容）”导出，或对单个关键请求用“复制响应/保存响应”落盘。"
        )

    prompt_tpl = (
        "你是一名严谨的信息抽取助手。给你一段网页接口返回的文本/JSON，请抽取结构化信息，只输出JSON对象，不要输出任何解释文字。\n"
        "安全要求：不要输出任何个人隐私信息（姓名/手机号/账号/地址等）。\n"
        "要求：\n"
        "1) codes 只能包含文本中明确出现的6位数字股票代码（不要猜）。\n"
        "2) names 提取文本中出现的股票名称/简称/谐音/缩写（原样保留）。\n"
        "3) topics 提取出现的题材/行业关键词（原样保留）。\n"
        "输出JSON格式：\n"
        '{ "time": "", "speaker": "", "codes": [], "names": [], "topics": [] }'
    )

    rows: List[Dict[str, object]] = []
    for e in entries:
        if not isinstance(e, dict):
            continue
        url, mime, status, text = _har_get_response_text(e)
        if not url or status < 200 or status >= 400:
            continue
        if url_contains and url_contains not in url:
            continue
        if "mx2025.hhhuu.com" not in url:
            continue
        if not text:
            continue
        if "application/json" not in mime and "json" not in mime.lower():
            continue
        if len(text) < 50:
            continue

        codes = sorted(set(re.findall(r"(?<!\d)(\d{6})(?!\d)", text)))
        safe_url = url.split("?", 1)[0]
        obj: Dict[str, object] = {
            "source_url": safe_url,
            "time": "",
            "speaker": "",
            "text": text[:200000],
            "codes": codes,
            "names": [],
            "topics": [],
        }
        lm = str(logic_model or "").strip()
        if lm and lm.lower() not in {"none", "off", "false", "0"}:
            resp2 = _ollama_generate(
                ollama_url=ollama_url,
                model=lm,
                prompt=prompt_tpl + "\n\n输入：\n" + obj["text"],
                images_b64=None,
                timeout_s=timeout_s,
            )
            try:
                obj2 = _extract_json_from_text(resp2)
                if isinstance(obj2, dict):
                    for k in ["time", "speaker", "names", "topics", "codes"]:
                        if k in obj2:
                            obj[k] = obj2[k]
            except Exception:
                pass
        rows.append(obj)

    out_jsonl.write_text("\n".join([json.dumps(x, ensure_ascii=False) for x in rows]) + ("\n" if rows else ""), encoding="utf-8")
    return out_jsonl


def build_factors_from_quicktiny_ladder(
    watchlist_dir: Path,
    min_height: int,
    top_n: int,
) -> Tuple[Path, pd.DataFrame]:
    data = _fetch_quicktiny_ladder()
    dates = data.get("dates", [])
    if not isinstance(dates, list) or not dates:
        raise ValueError("quicktiny ladder api missing dates")

    def _date_key(x: object) -> str:
        if not isinstance(x, dict):
            return ""
        return str(x.get("date", "") or "")

    latest = max(dates, key=_date_key)
    if not isinstance(latest, dict):
        raise ValueError("quicktiny ladder latest date payload invalid")
    date_tag = str(latest.get("date", "") or "")
    boards = latest.get("boards", [])
    if not isinstance(boards, list) or not boards:
        raise ValueError("quicktiny ladder latest payload missing boards")

    rows: List[Dict[str, object]] = []
    max_h = 0
    for b in boards:
        if not isinstance(b, dict):
            continue
        level = int(b.get("level", 0) or 0)
        stocks = b.get("stocks", [])
        if not isinstance(stocks, list):
            continue
        for s in stocks:
            if not isinstance(s, dict):
                continue
            code6 = _coerce_code6(s.get("code", ""))
            if not code6 or not _is_cn_retail_tradable(code6):
                continue
            h = int(s.get("continue_num", 0) or level or 0)
            max_h = max(max_h, h)
            open_num = int(s.get("open_num", 0) or 0)
            order_amount = float(s.get("order_amount", 0) or 0.0)
            turnover_rate = float(s.get("turnover_rate", 0) or 0.0)
            tags = s.get("tags", [])
            tag_str = ""
            if isinstance(tags, list):
                tag_str = ";".join([str(x) for x in tags if str(x).strip()])
            elif isinstance(tags, str):
                tag_str = tags
            rows.append(
                {
                    "code": code6,
                    "ticker": _to_ticker(code6),
                    "name": str(s.get("name", "") or ""),
                    "industry": str(s.get("industry", "") or ""),
                    "reason_type": str(s.get("reason_type", "") or ""),
                    "ladder_height": h,
                    "open_num": open_num,
                    "order_amount": order_amount,
                    "turnover_rate": turnover_rate,
                    "board_level": level,
                    "tags": tag_str,
                }
            )

    if not rows:
        raise ValueError("quicktiny ladder parsed empty rows")
    df = pd.DataFrame(rows)
    df = df.sort_values(["ladder_height"], ascending=[False]).reset_index(drop=True)

    if int(min_height) > 0:
        df = df[df["ladder_height"].fillna(0) >= int(min_height)].reset_index(drop=True)
    if len(df) == 0:
        raise ValueError("quicktiny ladder filtered empty; relax min_height")

    max_h_eff = int(max_h) if int(max_h) > 0 else int(df["ladder_height"].max() or 1)
    base = (df["ladder_height"].astype(float) / float(max_h_eff)).clip(0, 1)
    bonus = df["tags"].astype(str).apply(lambda x: 0.1 if ("总龙头" in x or "龙头" in x) else 0.0)
    penalty = pd.to_numeric(df.get("open_num", 0), errors="coerce").fillna(0).astype(float).clip(lower=0)
    penalty = (penalty.clip(upper=2) * 0.05).clip(0, 0.1)
    oa = pd.to_numeric(df.get("order_amount", 0), errors="coerce").fillna(0).astype(float).clip(lower=0)
    cap = float(oa.quantile(0.95)) if len(oa) else 0.0
    order_bonus = (oa.clip(upper=cap) / cap * 0.15) if cap > 0 else (oa * 0.0)
    tr = pd.to_numeric(df.get("turnover_rate", 0), errors="coerce").fillna(0).astype(float).clip(lower=0)
    tr_med = float(tr.median()) if len(tr) else 0.0
    tr_penalty = ((tr / tr_med - 1.0).clip(lower=0) * 0.05).clip(0, 0.10) if tr_med > 0 else (tr * 0.0)
    df["theme_score"] = (base + bonus - penalty + order_bonus - tr_penalty).clip(0, 1)
    df["source"] = "quicktiny_ladder"
    df["date"] = date_tag

    if int(top_n) > 0:
        df = df.head(int(top_n)).reset_index(drop=True)

    out = df[
        [
            "code",
            "ticker",
            "name",
            "theme_score",
            "ladder_height",
            "open_num",
            "order_amount",
            "turnover_rate",
            "industry",
            "reason_type",
            "tags",
            "source",
            "date",
        ]
    ].copy()
    out["fundamental_score"] = 0.0

    watchlist_dir.mkdir(parents=True, exist_ok=True)
    out_csv = watchlist_dir / f"factors_ladder_{date_tag or time.strftime('%Y%m%d')}.csv"
    out.to_csv(out_csv, index=False, encoding="utf-8-sig")
    return out_csv, out


def _decode_html(b: bytes) -> str:
    if not b:
        return ""
    for enc in ("utf-8", "gbk", "gb2312"):
        try:
            s = b.decode(enc)
            if "股票" in s or "阶段涨跌" in s or "<table" in s:
                return s
        except Exception:
            pass
    return b.decode("utf-8", errors="ignore")


def _strip_html(s: str) -> str:
    ss = re.sub(r"<\s*br\s*/?\s*>", "\n", s, flags=re.I)
    ss = re.sub(r"<[^>]+>", "", ss)
    ss = html.unescape(ss)
    ss = ss.replace("\xa0", " ").strip()
    ss = re.sub(r"\s+", " ", ss).strip()
    return ss


def _extract_sohu_asof(html_text: str) -> str:
    m = re.search(r"\[(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})\]", html_text)
    if m:
        return m.group(1).strip()
    ms = re.findall(r"(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2})", html_text)
    if ms:
        return str(ms[-1]).strip()
    return ""


def _parse_sohu_stage_rank_table(html_text: str) -> pd.DataFrame:
    tables = re.findall(r"(<table[\s\S]*?</table\s*>)", html_text, flags=re.I)
    target = ""
    for t in tables:
        if "股票代码" in t and "股票名称" in t and ("累积涨跌幅" in t or "累积涨跌" in t):
            target = t
            break
    if not target:
        raise ValueError("no stage-rank table found in html")

    rows = re.findall(r"(<tr[\s\S]*?</tr\s*>)", target, flags=re.I)
    parsed: List[Dict[str, object]] = []
    for r in rows:
        cells = re.findall(r"(<t[dh][\s\S]*?</t[dh]\s*>)", r, flags=re.I)
        if not cells:
            continue
        vals = [_strip_html(c) for c in cells]
        if vals and vals[0] == "排名":
            continue
        if len(vals) < 5:
            continue
        rank_s = vals[0]
        code = vals[1].strip()
        name = vals[2].strip()
        pct_s = vals[3].strip()
        price_s = vals[5].strip() if len(vals) > 5 else ""
        if not code.isdigit() or len(code) != 6:
            continue
        try:
            rank = int(re.sub(r"\D+", "", rank_s) or "0")
        except Exception:
            continue
        try:
            pct = float(pct_s.replace("%", "").replace("+", "").strip())
        except Exception:
            continue
        price = None
        if price_s:
            try:
                price = float(price_s)
            except Exception:
                price = None
        parsed.append({"rank": rank, "code": code, "name": name, "pct": pct, "price": price})

    if not parsed:
        raise ValueError("stage-rank table parsed empty")
    df = pd.DataFrame(parsed)
    df = df.sort_values(["pct", "rank"], ascending=[False, True]).reset_index(drop=True)
    return df


def _infer_exchange(code_6: str) -> str:
    c = (code_6 or "").strip()
    if c.startswith("6"):
        return "SH"
    if c.startswith(("0", "3")):
        return "SZ"
    if c.startswith(("8", "4")):
        return "BJ"
    return ""


def build_watchlist_top_gainers_week(top_n: int, watchlist_dir: Path) -> Tuple[Path, Path, pd.DataFrame]:
    urls = {
        "SH": "https://q.stock.sohu.com/cn/jdph/jdph_hushi_5d_00.shtml",
        "SZ": "https://q.stock.sohu.com/cn/jdph/jdph_shenshi_5d_00.shtml",
    }
    parts: List[pd.DataFrame] = []
    asof = ""
    for ex, url in urls.items():
        raw = _http_get(url)
        html_text = _decode_html(raw)
        if not asof:
            asof = _extract_sohu_asof(html_text)
        df = _parse_sohu_stage_rank_table(html_text)
        df["exchange"] = ex
        if ex == "SH":
            df = df[df["code"].astype(str).str.startswith("6")]
        if ex == "SZ":
            df = df[df["code"].astype(str).str.startswith(("0", "3"))]
        parts.append(df)

    all_df = pd.concat(parts, ignore_index=True)
    all_df["exchange"] = all_df["code"].astype(str).map(_infer_exchange)
    all_df["board"] = all_df["code"].astype(str).map(_board_tag)
    all_df["tradable"] = all_df["code"].astype(str).map(_is_cn_retail_tradable)
    all_df["ticker"] = all_df["code"].astype(str).map(_to_ticker)
    all_df = all_df.sort_values(["pct", "rank"], ascending=[False, True]).reset_index(drop=True)
    if top_n <= 0:
        top_n = 20
    out_df = all_df[all_df["tradable"]].head(int(top_n)).copy()
    out_df.insert(0, "top_rank", range(1, len(out_df) + 1))
    out_df["asof"] = asof
    out_df["source"] = "sohu_stage_rank_5d"

    watchlist_dir.mkdir(parents=True, exist_ok=True)
    date_tag = (asof.split(" ")[0].replace("-", "") if asof else time.strftime("%Y%m%d"))
    out_csv = watchlist_dir / f"top{top_n}_week_{date_tag}.csv"
    out_txt = watchlist_dir / f"top{top_n}_week_{date_tag}.txt"
    out_df.to_csv(out_csv, index=False, encoding="utf-8-sig")
    out_txt.write_text("\n".join(out_df["code"].astype(str).tolist()) + "\n", encoding="utf-8")
    return out_csv, out_txt, out_df


def _coerce_code6(x: object) -> str:
    s = str(x or "").strip()
    s = re.sub(r"\D+", "", s)
    if len(s) == 6:
        return s
    if len(s) < 6 and s.isdigit():
        return s.zfill(6)
    return ""


def _load_watchlist(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(str(path))
    suf = path.suffix.lower()
    if suf == ".txt":
        codes: List[str] = []
        for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
            c = _coerce_code6(line)
            if c:
                codes.append(c)
        if not codes:
            raise ValueError("watchlist txt parsed empty")
        out = pd.DataFrame({"code": codes, "name": [""] * len(codes)})
        out["ticker"] = out["code"].map(_to_ticker)
        out["board"] = out["code"].map(_board_tag)
        out["tradable"] = out["code"].map(_is_cn_retail_tradable)
        return out

    df0 = pd.read_csv(path)
    cols = list(df0.columns)
    code_col = _first_existing(cols, ["code", "股票代码", "证券代码", "ts_code"]) or ""
    if not code_col:
        raise ValueError("watchlist csv missing code column (code/股票代码/证券代码/ts_code)")
    name_col = _first_existing(cols, ["name", "股票名称", "名称"]) or ""
    out = pd.DataFrame()
    out["code"] = df0[code_col].map(_coerce_code6)
    out["name"] = df0[name_col].astype(str) if name_col else ""
    out = out[out["code"].astype(str).str.len() == 6].drop_duplicates(subset=["code"]).reset_index(drop=True)
    if len(out) == 0:
        raise ValueError("watchlist csv parsed empty")
    out["ticker"] = out["code"].map(_to_ticker)
    out["board"] = out["code"].map(_board_tag)
    out["tradable"] = out["code"].map(_is_cn_retail_tradable)
    return out


def _ret_n(close: pd.Series, n: int) -> Optional[float]:
    if n <= 0:
        return 0.0
    if len(close) < n + 1:
        return None
    a = float(close.iloc[-1])
    b = float(close.iloc[-(n + 1)])
    if b <= 0:
        return None
    return a / b - 1.0


def _vol_annualized(close: pd.Series, n: int) -> Optional[float]:
    if len(close) < n + 1:
        return None
    r = close.pct_change().dropna()
    r = r.iloc[-n:]
    if len(r) == 0:
        return None
    return float(r.std(ddof=0) * (252.0 ** 0.5))


def _max_drawdown(close: pd.Series, n: int) -> Optional[float]:
    if len(close) < 2:
        return None
    s = close.iloc[-n:] if n > 0 else close
    s = s.astype(float)
    peak = s.cummax()
    dd = s / peak - 1.0
    return float(dd.min())


def fetch_preprocess_and_screen_watchlist(
    watchlist_path: Path,
    output_dir: Path,
    watchlist_dir: Path,
    start_date: str,
    end_date: str,
    adjust: str,
    out_tag: str,
) -> Tuple[Path, pd.DataFrame]:
    wl = _load_watchlist(watchlist_path)
    rows: List[Dict[str, object]] = []
    try:
        import baostock as bs  # type: ignore
    except Exception as e:
        raise RuntimeError("baostock is not available. Install it in your venv first: pip install baostock") from e

    lg = bs.login()
    if getattr(lg, "error_code", "0") != "0":
        raise RuntimeError(f"baostock login failed: {getattr(lg,'error_msg','')}")
    try:
        for _, r in wl.iterrows():
            code6 = str(r["code"])
            name = str(r.get("name", "") or "")
            if not _is_cn_retail_tradable(code6):
                continue
            df0 = _fetch_baostock_1d_with_session(bs, symbol_6=code6, start=start_date, end=end_date, adjust=adjust)
            cfg = PrepConfig(
                output_dir=output_dir,
                symbol=code6,
                adjust_mode="none",
                date_col="",
                tz="Asia/Shanghai",
            )
            out_path, df = preprocess_one(cfg, df0=df0)
            close = pd.to_numeric(df["close"], errors="coerce").dropna()
            n_bars = int(len(close))
            last_date = df["date"].iloc[-1] if len(df) else None
            last_close = float(close.iloc[-1]) if len(close) else None
            ret_5d = _ret_n(close, 5)
            ret_20d = _ret_n(close, 20)
            vol_20d = _vol_annualized(close, 20)
            dd_60d = _max_drawdown(close, 60)
            avg_amount_20d = None
            if "amount" in df.columns:
                amt = pd.to_numeric(df["amount"], errors="coerce").dropna()
                if len(amt) >= 1:
                    avg_amount_20d = float(amt.iloc[-20:].mean())

            rows.append(
                {
                    "code": code6,
                    "name": name,
                    "exchange": _infer_exchange(code6),
                    "ticker": _to_ticker(code6),
                    "board": _board_tag(code6),
                    "tradable": True,
                    "n_bars": n_bars,
                    "last_date": str(pd.to_datetime(last_date).date()) if last_date is not None else "",
                    "last_close": last_close,
                    "ret_5d": ret_5d,
                    "ret_20d": ret_20d,
                    "vol_20d_ann": vol_20d,
                    "max_dd_60d": dd_60d,
                    "avg_amount_20d": avg_amount_20d,
                    "clean_csv": str(out_path),
                }
            )
    finally:
        bs.logout()

    out_df = pd.DataFrame(rows)
    out_df = out_df.sort_values(["ret_5d", "ret_20d"], ascending=[False, False]).reset_index(drop=True)
    watchlist_dir.mkdir(parents=True, exist_ok=True)
    date_tag = str(out_tag or "").strip() or time.strftime("%Y%m%d")
    out_csv = watchlist_dir / f"watchlist_screen_{date_tag}.csv"
    out_df.to_csv(out_csv, index=False, encoding="utf-8-sig")
    return out_csv, out_df


def build_focus_pool_from_screen(
    screen_csv: Path,
    watchlist_dir: Path,
    focus_n: int,
    min_avg_amount_20d: float,
    max_abs_dd_60d: float,
    min_bars: int,
    factor_csv: str,
    w_theme: float,
    w_fundamental: float,
    w_ret20: float,
    w_ret5: float,
    w_vol20: float,
    w_dd60: float,
    w_liq: float,
    out_tag: str,
) -> Tuple[Path, Path, pd.DataFrame]:
    df = pd.read_csv(screen_csv)
    if "code" not in df.columns:
        raise ValueError("screen csv missing 'code' column")
    df["code"] = df["code"].map(_coerce_code6)
    df = df[df["code"].astype(str).str.len() == 6].reset_index(drop=True)
    if "ticker" not in df.columns:
        df["ticker"] = df["code"].map(_to_ticker)
    if "board" not in df.columns:
        df["board"] = df["code"].map(_board_tag)
    if "tradable" not in df.columns:
        df["tradable"] = df["code"].map(_is_cn_retail_tradable)
    df = df[df["tradable"] == True].reset_index(drop=True)

    for c in ["ret_5d", "ret_20d", "vol_20d_ann", "max_dd_60d", "avg_amount_20d", "last_close", "n_bars"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    if "n_bars" in df.columns and int(min_bars) > 0:
        df = df[df["n_bars"].fillna(0) >= int(min_bars)]

    if "avg_amount_20d" in df.columns and min_avg_amount_20d > 0:
        df = df[df["avg_amount_20d"].fillna(0) >= float(min_avg_amount_20d)]

    if "max_dd_60d" in df.columns and max_abs_dd_60d > 0:
        df = df[df["max_dd_60d"].abs().fillna(10) <= float(max_abs_dd_60d)]

    if len(df) == 0:
        raise ValueError("focus pool filtered empty; relax filters")

    ret5 = df["ret_5d"].fillna(df["ret_5d"].median() if "ret_5d" in df.columns else 0)
    ret20 = df["ret_20d"].fillna(df["ret_20d"].median() if "ret_20d" in df.columns else 0)
    vol20 = df["vol_20d_ann"].fillna(df["vol_20d_ann"].median() if "vol_20d_ann" in df.columns else 0)
    dd60 = df["max_dd_60d"].fillna(df["max_dd_60d"].median() if "max_dd_60d" in df.columns else 0)
    liq = df["avg_amount_20d"].fillna(df["avg_amount_20d"].median() if "avg_amount_20d" in df.columns else 0)
    theme = pd.Series([0.0] * len(df), index=df.index)
    fundamental = pd.Series([0.0] * len(df), index=df.index)
    factor_path = str(factor_csv or "").strip()
    if factor_path:
        fdf0 = pd.read_csv(Path(factor_path))
        cols = list(fdf0.columns)
        code_col = _first_existing(cols, ["code", "股票代码", "证券代码"]) or ""
        if not code_col:
            raise ValueError("factor csv missing code column (code/股票代码/证券代码)")
        fdf = pd.DataFrame()
        fdf["code"] = fdf0[code_col].map(_coerce_code6)
        theme_col = _first_existing(cols, ["theme_score", "topic_score", "heat_score", "题材分", "热度分"]) or ""
        fund_col = _first_existing(cols, ["fundamental_score", "basic_score", "基本面分", "基本分"]) or ""
        if theme_col:
            fdf["theme_score"] = pd.to_numeric(fdf0[theme_col], errors="coerce")
        if fund_col:
            fdf["fundamental_score"] = pd.to_numeric(fdf0[fund_col], errors="coerce")
        fdf = fdf.dropna(subset=["code"]).drop_duplicates(subset=["code"])
        df = df.merge(fdf, on="code", how="left")
        if "theme_score" in df.columns:
            theme = pd.to_numeric(df["theme_score"], errors="coerce").fillna(0.0)
        if "fundamental_score" in df.columns:
            fundamental = pd.to_numeric(df["fundamental_score"], errors="coerce").fillna(0.0)

    def _z(s: pd.Series) -> pd.Series:
        std = float(s.std(ddof=0))
        if std <= 1e-12:
            return s * 0
        return (s - float(s.mean())) / std

    z_ret20 = _z(ret20)
    z_ret5 = _z(ret5)
    z_vol20 = _z(vol20)
    z_dd60 = _z(dd60.abs())
    z_liq = _z(liq)
    z_theme = _z(theme)
    z_fund = _z(fundamental)

    quant_score = (
        float(w_ret20) * z_ret20
        + float(w_ret5) * z_ret5
        + float(w_vol20) * z_vol20
        + float(w_dd60) * z_dd60
        + float(w_liq) * z_liq
    )
    theme_part = float(w_theme) * z_theme
    fund_part = float(w_fundamental) * z_fund
    score = quant_score + theme_part + fund_part
    df = df.copy()
    df["quant_score"] = quant_score
    df["theme_part"] = theme_part
    df["fund_part"] = fund_part
    df["score"] = score
    df = df.sort_values(["score", "ret_20d", "ret_5d"], ascending=[False, False, False]).reset_index(drop=True)
    df["score_pct"] = df["score"].rank(pct=True, ascending=True)

    if focus_n <= 0:
        focus_n = 5
    out_df = df.head(int(focus_n)).copy()
    out_df.insert(0, "focus_rank", range(1, len(out_df) + 1))

    watchlist_dir.mkdir(parents=True, exist_ok=True)
    date_tag = str(out_tag or "").strip() or time.strftime("%Y%m%d")
    out_csv = watchlist_dir / f"focus_pool_{date_tag}.csv"
    out_txt = watchlist_dir / f"focus_pool_{date_tag}.txt"
    out_df.to_csv(out_csv, index=False, encoding="utf-8-sig")
    out_txt.write_text("\n".join(out_df["code"].astype(str).tolist()) + "\n", encoding="utf-8")
    return out_csv, out_txt, out_df


def build_core_pool_from_focus_history(
    watchlist_dir: Path,
    current_tag: str,
    current_screen_df: pd.DataFrame,
    current_focus_df: pd.DataFrame,
    window_days: int,
    min_appear: int,
    min_score_pct: float,
    min_bars: int,
    min_avg_amount_20d: float,
    max_abs_dd_60d: float,
    max_core_n: int,
) -> Tuple[Path, Path, pd.DataFrame]:
    watchlist_dir.mkdir(parents=True, exist_ok=True)
    files = list(watchlist_dir.glob("focus_pool_*.csv"))
    if not files:
        out = pd.DataFrame(columns=["core_rank", "ticker", "code", "name", "appear", "good_appear"])
        out_csv = watchlist_dir / f"core_pool_{current_tag}.csv"
        out_txt = watchlist_dir / f"core_pool_{current_tag}.txt"
        out.to_csv(out_csv, index=False, encoding="utf-8-sig")
        out_txt.write_text("", encoding="utf-8")
        return out_csv, out_txt, out

    def _tag_from_name(p: Path) -> str:
        m = re.search(r"focus_pool_(\d{8})\.csv$", p.name)
        return m.group(1) if m else ""

    tagged = [(p, _tag_from_name(p)) for p in files]
    tagged = [(p, t) for (p, t) in tagged if t]
    tagged.sort(key=lambda x: x[1], reverse=True)
    tagged = tagged[: max(int(window_days), 1)]

    appear: Dict[str, int] = {}
    good: Dict[str, int] = {}
    last_seen: Dict[str, str] = {}
    for p, t in tagged:
        try:
            df = pd.read_csv(p)
        except Exception:
            continue
        if "code" not in df.columns:
            continue
        df["code"] = df["code"].map(_coerce_code6)
        for _, r in df.iterrows():
            code6 = str(r.get("code", "") or "")
            if len(code6) != 6:
                continue
            appear[code6] = int(appear.get(code6, 0)) + 1
            last_seen[code6] = max(str(last_seen.get(code6, "")), t)
            sp = r.get("score_pct", None)
            try:
                spv = float(sp)
            except Exception:
                spv = None
            if spv is not None and float(min_score_pct) > 0 and spv >= float(min_score_pct):
                good[code6] = int(good.get(code6, 0)) + 1

    rows: List[Dict[str, object]] = []
    for code6, c in appear.items():
        g = int(good.get(code6, 0))
        if int(min_score_pct) > 0:
            if g < int(min_appear):
                continue
        if c < int(min_appear):
            continue
        rows.append({"code": code6, "appear": c, "good_appear": g, "last_seen": last_seen.get(code6, "")})

    if not rows:
        out = pd.DataFrame(columns=["core_rank", "ticker", "code", "name", "appear", "good_appear"])
        out_csv = watchlist_dir / f"core_pool_{current_tag}.csv"
        out_txt = watchlist_dir / f"core_pool_{current_tag}.txt"
        out.to_csv(out_csv, index=False, encoding="utf-8-sig")
        out_txt.write_text("", encoding="utf-8")
        return out_csv, out_txt, out

    hist = pd.DataFrame(rows)

    screen = current_screen_df.copy()
    if "code" not in screen.columns:
        raise ValueError("current screen df missing code")
    screen["code"] = screen["code"].map(_coerce_code6)
    if "ticker" not in screen.columns:
        screen["ticker"] = screen["code"].map(_to_ticker)
    if "name" not in screen.columns:
        screen["name"] = ""
    for c in ["n_bars", "avg_amount_20d", "max_dd_60d"]:
        if c in screen.columns:
            screen[c] = pd.to_numeric(screen[c], errors="coerce")

    out = hist.merge(screen, on="code", how="left")
    if int(min_bars) > 0 and "n_bars" in out.columns:
        out = out[out["n_bars"].fillna(0) >= int(min_bars)]
    if float(min_avg_amount_20d) > 0 and "avg_amount_20d" in out.columns:
        out = out[out["avg_amount_20d"].fillna(0) >= float(min_avg_amount_20d)]
    if float(max_abs_dd_60d) > 0 and "max_dd_60d" in out.columns:
        out = out[out["max_dd_60d"].abs().fillna(10) <= float(max_abs_dd_60d)]

    if "score" in current_focus_df.columns:
        cf = current_focus_df[["code", "score"]].copy()
        cf["code"] = cf["code"].map(_coerce_code6)
        out = out.merge(cf, on="code", how="left", suffixes=("", "_today"))

    out = out.sort_values(["appear", "good_appear", "score"], ascending=[False, False, False]).reset_index(drop=True)
    if int(max_core_n) > 0:
        out = out.head(int(max_core_n)).reset_index(drop=True)
    out.insert(0, "core_rank", range(1, len(out) + 1))

    keep_cols = ["core_rank", "ticker", "code", "name", "appear", "good_appear", "n_bars", "avg_amount_20d", "max_dd_60d", "score"]
    keep_cols = [c for c in keep_cols if c in out.columns]
    out2 = out[keep_cols].copy()

    out_csv = watchlist_dir / f"core_pool_{current_tag}.csv"
    out_txt = watchlist_dir / f"core_pool_{current_tag}.txt"
    out2.to_csv(out_csv, index=False, encoding="utf-8-sig")
    out_txt.write_text("\n".join(out2["code"].astype(str).tolist()) + "\n" if len(out2) else "", encoding="utf-8")
    return out_csv, out_txt, out2


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--out-tag", default="")
    p.add_argument("--weekly-top", action="store_true")
    p.add_argument("--top-n", type=int, default=20)
    p.add_argument("--watchlist-dir", default=str(Path("data") / "ashare_watchlist"))
    p.add_argument("--watchlist-fetch", action="store_true")
    p.add_argument("--watchlist", default="")
    p.add_argument("--ladder-factors", action="store_true")
    p.add_argument("--ladder-min-height", type=int, default=2)
    p.add_argument("--ladder-top-n", type=int, default=60)
    p.add_argument("--ladder-daily", action="store_true")
    p.add_argument("--ladder-healthcheck", action="store_true")
    p.add_argument("--healthcheck-n", type=int, default=10)
    p.add_argument("--blogroom-summarize", action="store_true")
    p.add_argument("--blogroom-aggregate", action="store_true")
    p.add_argument("--mx2025-from-har", action="store_true")
    p.add_argument("--blogroom-dir", default=str(Path("A股博客直播间")))
    p.add_argument("--blogroom-jsonl", default="")
    p.add_argument("--blogroom-min-count", type=int, default=2)
    p.add_argument("--mx2025-har", default="")
    p.add_argument("--mx2025-url-contains", default="")
    p.add_argument("--ollama-url", default="http://localhost:11434")
    p.add_argument("--ollama-model", default="llama3.2-vision")
    p.add_argument("--blogroom-logic-model", default="qwen2.5:32b-instruct")
    p.add_argument("--blogroom-ocr", default="ollama", choices=["ollama", "easyocr"])
    p.add_argument("--blogroom-max-images", type=int, default=30)
    p.add_argument("--blogroom-timeout-s", type=int, default=600)
    p.add_argument("--focus-from-screen", default="")
    p.add_argument("--focus-n", type=int, default=5)
    p.add_argument("--min-avg-amount-20d", type=float, default=0.0)
    p.add_argument("--max-abs-dd-60d", type=float, default=0.0)
    p.add_argument("--min-bars", type=int, default=0)
    p.add_argument("--factor-csv", default="")
    p.add_argument("--w-theme", type=float, default=0.0)
    p.add_argument("--w-fundamental", type=float, default=0.0)
    p.add_argument("--w-ret20", type=float, default=0.30)
    p.add_argument("--w-ret5", type=float, default=0.25)
    p.add_argument("--w-vol20", type=float, default=-0.20)
    p.add_argument("--w-dd60", type=float, default=-0.15)
    p.add_argument("--w-liq", type=float, default=0.10)
    p.add_argument("--core-window-days", type=int, default=5)
    p.add_argument("--core-min-appear", type=int, default=3)
    p.add_argument("--core-min-score-pct", type=float, default=0.80)
    p.add_argument("--core-min-bars", type=int, default=120)
    p.add_argument("--core-min-avg-amount-20d", type=float, default=0.0)
    p.add_argument("--core-max-abs-dd-60d", type=float, default=0.30)
    p.add_argument("--core-max-n", type=int, default=10)
    p.add_argument("--input", default="")
    p.add_argument("--fetch", default="none", choices=["none", "akshare", "baostock"])
    p.add_argument("--output-dir", default=str(Path("data") / "ashare_clean"))
    p.add_argument("--symbol", default="")
    p.add_argument("--adjust", default="none", choices=["none", "qfq", "hfq"])
    p.add_argument("--start-date", default="")
    p.add_argument("--end-date", default="")
    p.add_argument("--date-col", default="")
    p.add_argument("--tz", default="Asia/Shanghai")
    args = p.parse_args(argv)

    try:
        if bool(getattr(args, "weekly_top", False)):
            out_csv, out_txt, out_df = build_watchlist_top_gainers_week(
                top_n=int(getattr(args, "top_n", 20) or 20),
                watchlist_dir=Path(str(getattr(args, "watchlist_dir", ""))),
            )
            print(f"[A_SHARE_PREP] ok weekly_top={len(out_df)} out_csv={out_csv} out_txt={out_txt}")
            for _, r in out_df.iterrows():
                pct_s = f"{float(r['pct']):.2f}%"
                px = r.get("price", None)
                px_s = f"{float(px):.2f}" if px is not None and str(px) != "nan" else ""
                ticker = str(r.get("ticker", "") or r.get("code", ""))
                print(f"[A_SHARE_PREP] {int(r['top_rank']):02d} {ticker} {r['name']} pct_5d={pct_s} price={px_s}")
            return 0

        if bool(getattr(args, "ladder_healthcheck", False)):
            res = ladder_healthcheck_quicktiny(n=int(getattr(args, "healthcheck_n", 10) or 10))
            print(
                "[A_SHARE_PREP] ladder_healthcheck "
                + " ".join(
                    [
                        f"n={res.get('n')}",
                        f"ok_runs={res.get('ok_runs')}",
                        f"missing_runs={res.get('missing_runs')}",
                        f"p50_s={float(res.get('p50_s',0.0)):.3f}",
                        f"p95_s={float(res.get('p95_s',0.0)):.3f}",
                        f"max_s={float(res.get('max_s',0.0)):.3f}",
                    ]
                )
            )
            if res.get("missing_runs", 0):
                print(f"[A_SHARE_PREP] last_missing={res.get('last_missing')}")
            keys = res.get("sample_stock_keys", [])
            if isinstance(keys, list) and keys:
                print(f"[A_SHARE_PREP] sample_stock_keys={','.join([str(x) for x in keys[:30]])}")
            return 0

        if bool(getattr(args, "blogroom_summarize", False)):
            out_dir = Path(str(getattr(args, "watchlist_dir", "")))
            out_jsonl, out_codes = blogroom_summarize_with_ollama(
                blogroom_dir=Path(str(getattr(args, "blogroom_dir", ""))),
                out_dir=out_dir,
                out_tag=str(getattr(args, "out_tag", "") or "").strip(),
                ollama_url=str(getattr(args, "ollama_url", "") or ""),
                ollama_model=str(getattr(args, "ollama_model", "") or ""),
                logic_model=str(getattr(args, "blogroom_logic_model", "") or ""),
                ocr_mode=str(getattr(args, "blogroom_ocr", "") or ""),
                max_images=int(getattr(args, "blogroom_max_images", 30) or 30),
                timeout_s=int(getattr(args, "blogroom_timeout_s", 120) or 120),
            )
            print(f"[A_SHARE_PREP] ok blogroom_summarize out_jsonl={out_jsonl} out_codes={out_codes}")
            return 0

        if bool(getattr(args, "blogroom_aggregate", False)):
            out_dir = Path(str(getattr(args, "watchlist_dir", "")))
            sp = str(getattr(args, "blogroom_jsonl", "") or "").strip()
            summary_jsonl = Path(sp) if sp else None
            if summary_jsonl is None:
                files = list(out_dir.glob("blogroom_summary_*.jsonl"))
                if not files:
                    raise ValueError(f"no blogroom_summary_*.jsonl found in {out_dir}")
                files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
                summary_jsonl = files[0]
            out_topics, out_names = blogroom_aggregate_jsonl(
                summary_jsonl=summary_jsonl,
                out_dir=out_dir,
                out_tag=str(getattr(args, "out_tag", "") or "").strip(),
                min_count=int(getattr(args, "blogroom_min_count", 2) or 2),
            )
            print(f"[A_SHARE_PREP] ok blogroom_aggregate in_jsonl={summary_jsonl} out_topics={out_topics} out_names={out_names}")
            return 0

        if bool(getattr(args, "mx2025_from_har", False)):
            hp = str(getattr(args, "mx2025_har", "") or "").strip()
            if not hp:
                raise ValueError("--mx2025-har is required when --mx2025-from-har is set")
            out_dir = Path(str(getattr(args, "watchlist_dir", "")))
            out_jsonl = mx2025_extract_from_har(
                har_path=Path(hp),
                out_dir=out_dir,
                out_tag=str(getattr(args, "out_tag", "") or "").strip(),
                ollama_url=str(getattr(args, "ollama_url", "") or ""),
                logic_model=str(getattr(args, "blogroom_logic_model", "") or ""),
                timeout_s=int(getattr(args, "blogroom_timeout_s", 600) or 600),
                url_contains=str(getattr(args, "mx2025_url_contains", "") or ""),
            )
            print(f"[A_SHARE_PREP] ok mx2025_from_har out_jsonl={out_jsonl}")
            return 0

        if bool(getattr(args, "watchlist_fetch", False)):
            wp = Path(str(getattr(args, "watchlist", "") or "")).expanduser()
            if not str(wp):
                raise ValueError("--watchlist is required when --watchlist-fetch is set")
            out_csv, out_df = fetch_preprocess_and_screen_watchlist(
                watchlist_path=wp,
                output_dir=Path(str(getattr(args, "output_dir", ""))),
                watchlist_dir=Path(str(getattr(args, "watchlist_dir", ""))),
                start_date=str(getattr(args, "start_date", "") or ""),
                end_date=str(getattr(args, "end_date", "") or ""),
                adjust=str(getattr(args, "adjust", "none") or "none"),
                out_tag=str(getattr(args, "out_tag", "") or ""),
            )
            print(f"[A_SHARE_PREP] ok watchlist_fetch={len(out_df)} screen_csv={out_csv}")
            for i, r in out_df.head(20).iterrows():
                ret5 = r.get("ret_5d", None)
                ret5_s = f"{float(ret5) * 100:.2f}%" if ret5 is not None and str(ret5) != "nan" else ""
                lc = r.get("last_close", None)
                lc_s = f"{float(lc):.2f}" if lc is not None and str(lc) != "nan" else ""
                ticker = str(r.get("ticker", "") or r.get("code", ""))
                print(f"[A_SHARE_PREP] {int(i)+1:02d} {ticker} {r.get('name','')} last={lc_s} ret_5d={ret5_s}")
            return 0

        if bool(getattr(args, "ladder_factors", False)):
            out_csv, out_df = build_factors_from_quicktiny_ladder(
                watchlist_dir=Path(str(getattr(args, "watchlist_dir", ""))),
                min_height=int(getattr(args, "ladder_min_height", 2) or 2),
                top_n=int(getattr(args, "ladder_top_n", 60) or 60),
            )
            print(f"[A_SHARE_PREP] ok ladder_factors={len(out_df)} out_csv={out_csv}")
            for i, r in out_df.head(20).iterrows():
                sc = r.get("theme_score", None)
                sc_s = f"{float(sc):.2f}" if sc is not None and str(sc) != "nan" else ""
                h = r.get("ladder_height", None)
                h_s = f"{int(h)}" if h is not None and str(h) != "nan" else ""
                print(f"[A_SHARE_PREP] {int(i)+1:02d} {r.get('ticker','')} {r.get('name','')} theme={sc_s} height={h_s} industry={r.get('industry','')}")
            return 0

        if bool(getattr(args, "ladder_daily", False)):
            watchlist_dir = Path(str(getattr(args, "watchlist_dir", "")))
            factors_csv, fdf = build_factors_from_quicktiny_ladder(
                watchlist_dir=watchlist_dir,
                min_height=int(getattr(args, "ladder_min_height", 2) or 2),
                top_n=int(getattr(args, "ladder_top_n", 60) or 60),
            )
            ladder_tag = str(fdf["date"].iloc[0] if len(fdf) else "").strip()
            if not ladder_tag:
                ladder_tag = time.strftime("%Y%m%d")

            screen_csv, screen_df = fetch_preprocess_and_screen_watchlist(
                watchlist_path=Path(str(factors_csv)),
                output_dir=Path(str(getattr(args, "output_dir", ""))),
                watchlist_dir=watchlist_dir,
                start_date=str(getattr(args, "start_date", "") or ""),
                end_date=str(getattr(args, "end_date", "") or ""),
                adjust=str(getattr(args, "adjust", "none") or "none"),
                out_tag=ladder_tag,
            )
            focus_csv, focus_txt, focus_df = build_focus_pool_from_screen(
                screen_csv=Path(str(screen_csv)),
                watchlist_dir=watchlist_dir,
                focus_n=int(getattr(args, "focus_n", 5) or 5),
                min_avg_amount_20d=float(getattr(args, "min_avg_amount_20d", 0.0) or 0.0),
                max_abs_dd_60d=float(getattr(args, "max_abs_dd_60d", 0.0) or 0.0),
                min_bars=int(getattr(args, "min_bars", 0) or 0),
                factor_csv=str(factors_csv),
                w_theme=float(getattr(args, "w_theme", 0.0) or 0.0),
                w_fundamental=float(getattr(args, "w_fundamental", 0.0) or 0.0),
                w_ret20=float(getattr(args, "w_ret20", 0.30) or 0.30),
                w_ret5=float(getattr(args, "w_ret5", 0.25) or 0.25),
                w_vol20=float(getattr(args, "w_vol20", -0.20) or -0.20),
                w_dd60=float(getattr(args, "w_dd60", -0.15) or -0.15),
                w_liq=float(getattr(args, "w_liq", 0.10) or 0.10),
                out_tag=ladder_tag,
            )
            print(f"[A_SHARE_PREP] ok ladder_daily tag={ladder_tag}")
            print(f"[A_SHARE_PREP] ladder_factors_csv={factors_csv}")
            print(f"[A_SHARE_PREP] watchlist_screen_csv={screen_csv}")
            print(f"[A_SHARE_PREP] focus_csv={focus_csv} focus_txt={focus_txt}")
            for _, r in focus_df.iterrows():
                sc = r.get("score", None)
                sc_s = f"{float(sc):.3f}" if sc is not None and str(sc) != "nan" else ""
                qs = r.get("quant_score", None)
                qs_s = f"{float(qs):.3f}" if qs is not None and str(qs) != "nan" else ""
                tp = r.get("theme_part", None)
                tp_s = f"{float(tp):.3f}" if tp is not None and str(tp) != "nan" else ""
                ret5 = r.get("ret_5d", None)
                ret5_s = f"{float(ret5) * 100:.2f}%" if ret5 is not None and str(ret5) != "nan" else ""
                ret20 = r.get("ret_20d", None)
                ret20_s = f"{float(ret20) * 100:.2f}%" if ret20 is not None and str(ret20) != "nan" else ""
                dd60 = r.get("max_dd_60d", None)
                dd60_s = f"{float(dd60) * 100:.2f}%" if dd60 is not None and str(dd60) != "nan" else ""
                ticker = str(r.get("ticker", "") or r.get("code", ""))
                print(f"[A_SHARE_PREP] {int(r['focus_rank']):02d} {ticker} {r.get('name','')} score={sc_s} q={qs_s} theme_part={tp_s} ret_5d={ret5_s} ret_20d={ret20_s} dd_60d={dd60_s}")

            core_csv, core_txt, core_df = build_core_pool_from_focus_history(
                watchlist_dir=watchlist_dir,
                current_tag=ladder_tag,
                current_screen_df=screen_df,
                current_focus_df=focus_df,
                window_days=int(getattr(args, "core_window_days", 5) or 5),
                min_appear=int(getattr(args, "core_min_appear", 3) or 3),
                min_score_pct=float(getattr(args, "core_min_score_pct", 0.80) or 0.80),
                min_bars=int(getattr(args, "core_min_bars", 120) or 120),
                min_avg_amount_20d=float(getattr(args, "core_min_avg_amount_20d", 0.0) or 0.0),
                max_abs_dd_60d=float(getattr(args, "core_max_abs_dd_60d", 0.30) or 0.30),
                max_core_n=int(getattr(args, "core_max_n", 10) or 10),
            )
            print(f"[A_SHARE_PREP] core_csv={core_csv} core_txt={core_txt} core_n={len(core_df)}")
            for _, r in core_df.iterrows():
                ticker = str(r.get("ticker", "") or r.get("code", ""))
                print(f"[A_SHARE_PREP] CORE {int(r.get('core_rank',0)):02d} {ticker} {r.get('name','')} appear={int(r.get('appear',0))}/{int(getattr(args,'core_window_days',5) or 5)} good={int(r.get('good_appear',0))}")
            return 0

        if str(getattr(args, "focus_from_screen", "") or "").strip():
            out_csv, out_txt, out_df = build_focus_pool_from_screen(
                screen_csv=Path(str(getattr(args, "focus_from_screen", ""))),
                watchlist_dir=Path(str(getattr(args, "watchlist_dir", ""))),
                focus_n=int(getattr(args, "focus_n", 5) or 5),
                min_avg_amount_20d=float(getattr(args, "min_avg_amount_20d", 0.0) or 0.0),
                max_abs_dd_60d=float(getattr(args, "max_abs_dd_60d", 0.0) or 0.0),
                min_bars=int(getattr(args, "min_bars", 0) or 0),
                factor_csv=str(getattr(args, "factor_csv", "") or ""),
                w_theme=float(getattr(args, "w_theme", 0.0) or 0.0),
                w_fundamental=float(getattr(args, "w_fundamental", 0.0) or 0.0),
                w_ret20=float(getattr(args, "w_ret20", 0.30) or 0.30),
                w_ret5=float(getattr(args, "w_ret5", 0.25) or 0.25),
                w_vol20=float(getattr(args, "w_vol20", -0.20) or -0.20),
                w_dd60=float(getattr(args, "w_dd60", -0.15) or -0.15),
                w_liq=float(getattr(args, "w_liq", 0.10) or 0.10),
                out_tag=str(getattr(args, "out_tag", "") or ""),
            )
            print(f"[A_SHARE_PREP] ok focus_pool={len(out_df)} out_csv={out_csv} out_txt={out_txt}")
            for _, r in out_df.iterrows():
                sc = r.get("score", None)
                sc_s = f"{float(sc):.3f}" if sc is not None and str(sc) != "nan" else ""
                qs = r.get("quant_score", None)
                qs_s = f"{float(qs):.3f}" if qs is not None and str(qs) != "nan" else ""
                tp = r.get("theme_part", None)
                tp_s = f"{float(tp):.3f}" if tp is not None and str(tp) != "nan" else ""
                ret5 = r.get("ret_5d", None)
                ret5_s = f"{float(ret5) * 100:.2f}%" if ret5 is not None and str(ret5) != "nan" else ""
                ret20 = r.get("ret_20d", None)
                ret20_s = f"{float(ret20) * 100:.2f}%" if ret20 is not None and str(ret20) != "nan" else ""
                dd60 = r.get("max_dd_60d", None)
                dd60_s = f"{float(dd60) * 100:.2f}%" if dd60 is not None and str(dd60) != "nan" else ""
                ticker = str(r.get("ticker", "") or r.get("code", ""))
                print(f"[A_SHARE_PREP] {int(r['focus_rank']):02d} {ticker} {r.get('name','')} score={sc_s} q={qs_s} theme_part={tp_s} ret_5d={ret5_s} ret_20d={ret20_s} dd_60d={dd60_s}")
            return 0

        df0, source = _load_input_df(args)
        effective_adjust = "none" if source in {"akshare", "baostock"} else str(args.adjust or "none")

        cfg = PrepConfig(
            output_dir=Path(args.output_dir),
            symbol=str(args.symbol or ""),
            adjust_mode=effective_adjust,
            date_col=str(args.date_col or ""),
            tz=str(args.tz or "Asia/Shanghai"),
        )
        out_path, df = preprocess_one(cfg, df0=df0)
        first = df["date"].iloc[0].to_pydatetime() if len(df) else None
        last = df["date"].iloc[-1].to_pydatetime() if len(df) else None
        print(f"[A_SHARE_PREP] ok symbol={df['symbol'].iloc[0] if len(df) else ''} rows={len(df)} out={out_path}")
        print(f"[A_SHARE_PREP] range {first} -> {last}")
        return 0
    except Exception as e:
        print(f"[A_SHARE_PREP][ERROR] {type(e).__name__}: {e}")
        if bool(getattr(args, "weekly_top", False)):
            print("[A_SHARE_PREP][HINT] 获取涨幅榜失败时可选处理：")
            print("  1) 稍后重试（可能是网络/站点临时波动）")
            print("  2) 换网络/代理（公司代理可能拦截）")
            print("  3) 临时兜底：我可以改成用本地全市场日线来算（需要你先有全市场日线数据）")
        if bool(getattr(args, "watchlist_fetch", False)):
            print("[A_SHARE_PREP][HINT] watchlist-fetch 失败时可选处理：")
            print("  1) 先跑 --weekly-top 生成 watchlist 文件，再用 --watchlist <csv/txt>")
            print("  2) 缩短区间：加 --start-date 2024-01-01 --end-date 2026-05-09")
            print("  3) 如果某只票失败：先删掉该票再跑（或我再加“跳过失败标的”的开关）")
        if bool(getattr(args, "ladder_factors", False)):
            print("[A_SHARE_PREP][HINT] ladder-factors 失败时可选处理：")
            print("  1) 稍后重试（站点可能临时波动）")
            print("  2) 检查网络/公司代理是否拦截 https://stock.quicktiny.cn")
        if bool(getattr(args, "ladder_healthcheck", False)):
            print("[A_SHARE_PREP][HINT] ladder-healthcheck 失败时可选处理：")
            print("  1) 稍后重试（站点可能临时波动）")
            print("  2) 检查网络/公司代理是否拦截 https://stock.quicktiny.cn")
        if bool(getattr(args, "blogroom_summarize", False)):
            print("[A_SHARE_PREP][HINT] blogroom-summarize 失败时可选处理：")
            print("  1) 确认本机已安装并启动 Ollama（默认地址 http://localhost:11434）")
            print("  2) 拉取并使用视觉模型（示例）：ollama pull llama3.2-vision")
            print("  3) 若模型名不同：用 --ollama-model <name> 指定；地址不同：用 --ollama-url <url> 指定")
            print("  4) 确认 --blogroom-dir 指向包含截图的目录（支持 .png/.jpg/.jpeg/.webp）")
            print("  5) 若视觉模型对中文OCR效果差：用 --blogroom-ocr easyocr，并先安装：.\\.venv\\Scripts\\python.exe -m pip install easyocr")
        if str(getattr(args, "fetch", "none") or "none").strip().lower() == "akshare":
            print("[A_SHARE_PREP][HINT] 数据源可能临时断连/限流。可选处理：")
            print("  1) 原命令重试（隔 1-3 分钟再跑一次）")
            print("  2) 缩短区间：加 --start-date 20200101 --end-date 20260508")
            print("  3) 换成本地CSV：先导出日线CSV，再用 --input <path> 运行")
        if str(getattr(args, "fetch", "none") or "none").strip().lower() == "baostock":
            print("[A_SHARE_PREP][HINT] 可选处理：")
            print("  1) 检查网络/公司代理，或稍后重试")
            print("  2) 缩短区间：加 --start-date 2020-01-01 --end-date 2026-05-08")
            print("  3) 换成本地CSV：先导出日线CSV，再用 --input <path> 运行")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
