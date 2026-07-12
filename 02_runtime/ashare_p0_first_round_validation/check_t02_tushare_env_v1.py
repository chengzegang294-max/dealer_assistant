from __future__ import annotations

import argparse
import importlib
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
DEFAULT_OUTPUT_DIR = ROOT / "artifacts" / "t02_tushare_preflight"


def load_tushare_token() -> tuple[str | None, str]:
    env_token = (os.environ.get("TUSHARE_TOKEN") or "").strip()
    if env_token:
        return env_token, "env:TUSHARE_TOKEN"

    home_token = Path.home() / ".tushare" / "token"
    if home_token.exists():
        token = home_token.read_text(encoding="utf-8").strip()
        if token:
            return token, str(home_token)

    return None, "missing"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def probe_import(module_name: str) -> dict[str, Any]:
    try:
        importlib.import_module(module_name)
        return {"available": True, "detail": ""}
    except Exception as exc:  # pragma: no cover
        return {"available": False, "detail": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check whether local T02 Tushare fetchers can run before hitting API."
    )
    parser.add_argument(
        "--output-dir",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directory for preflight JSON output.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_path = output_dir / "t02_tushare_preflight_latest.json"

    token, token_source = load_tushare_token()
    pandas_probe = probe_import("pandas")
    tushare_probe = probe_import("tushare")

    payload: dict[str, Any] = {
        "producer": "check_t02_tushare_env_v1.py",
        "scope": "A股 P0 首轮离线验证 T02 Tushare 抓取环境预检",
        "status": "started",
        "token_source": token_source,
        "token_present": bool(token),
        "dependency_status": {
            "pandas": pandas_probe,
            "tushare": tushare_probe,
        },
        "output_json": str(output_path).replace("\\", "/"),
        "recommended_fetchers": [
            "fetch_t02_moneyflow_tushare_v1.py",
            "fetch_t02_northbound_tushare_v1.py",
            "fetch_t02_industry_map_tushare_v1.py",
        ],
    }

    missing_modules = [
        name
        for name, result in {
            "pandas": pandas_probe,
            "tushare": tushare_probe,
        }.items()
        if not result["available"]
    ]

    blockers: list[str] = []
    if not token:
        blockers.append("tushare_token_missing")
    if missing_modules:
        blockers.append("dependency_import_failed")

    if blockers:
        payload["status"] = "failed"
        payload["failure_reason"] = blockers[0]
        payload["blockers"] = blockers
        if missing_modules:
            payload["missing_modules"] = missing_modules
        payload["next_action"] = "set TUSHARE_TOKEN, install missing packages, then rerun preflight"
        write_json(output_path, payload)
        return 2 if not token else 3

    payload["status"] = "ready"
    payload["next_action"] = "run the T02 Tushare fetchers"
    write_json(output_path, payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
