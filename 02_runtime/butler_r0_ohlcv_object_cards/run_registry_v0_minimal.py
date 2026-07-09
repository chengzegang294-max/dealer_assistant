from __future__ import annotations

import argparse
import json
from pathlib import Path

from run_object_card_minimal_v1 import calc_bpb, calc_volfac, load_ohlcv_rows
from run_period_queen_proxy_minimal_v1 import calc_output as calc_period_queen_proxy
from run_tkr7_minimal_v1 import calc_output as calc_tkr7
from run_voltarget_minimal_v1 import calc_output as calc_voltarget
from run_vp_minimal_v1 import calc_output as calc_vp


def normalize_volfac(result: dict[str, object]) -> dict[str, object]:
    payload = result["signal_payload"]
    assert isinstance(payload, dict)
    return {
        "object_id": "VOLFAC_P0_A",
        "card_role": "filter",
        "signal_type": str(payload.get("signal_type", "FILTER")),
        "signal_direction": "sell" if float(payload.get("signal_strength", 0)) < 0 else "buy" if float(payload.get("signal_strength", 0)) > 0 else "neutral",
        "signal_strength": abs(float(payload.get("signal_strength", 0))),
        "confidence": float(payload.get("confidence", 0)),
        "filter_action": payload.get("filter_action", "PASS"),
        "risk_action": payload.get("risk_action", "NONE"),
        "size_scalar": float(payload.get("size_scalar", 1.0)),
        "detail": payload,
    }


def normalize_bpb(result: dict[str, object]) -> dict[str, object]:
    payload = result["signal_payload"]
    assert isinstance(payload, dict)
    signal_type = str(payload.get("bpb_signal_type", "WAITING"))
    if signal_type == "BPB":
        direction = "buy"
    elif signal_type in {"BOF", "TOO_DEEP"}:
        direction = "sell"
    else:
        direction = "neutral"
    return {
        "object_id": "BPB_P0_E",
        "card_role": "voter",
        "signal_type": signal_type,
        "signal_direction": direction,
        "signal_strength": float(payload.get("bpb_signal_strength", 0)),
        "confidence": 0.72 if direction != "neutral" else 0.55,
        "filter_action": "PASS",
        "risk_action": "NONE",
        "size_scalar": 1.0,
        "detail": payload,
    }


def normalize_vp(result: dict[str, object]) -> dict[str, object]:
    payload = result["signal_payload"]
    assert isinstance(payload, dict)
    signal_type = str(payload.get("vp_signal_type", "NONE"))
    direction = "buy" if signal_type in {"VA_BREAKOUT", "POC_REVERSION", "LVN_MOMENTUM"} else "neutral"
    return {
        "object_id": "VP_P0_E",
        "card_role": "voter",
        "signal_type": signal_type,
        "signal_direction": direction,
        "signal_strength": float(payload.get("vp_signal_strength", 0)),
        "confidence": 0.68 if direction == "buy" else 0.5,
        "filter_action": "PASS",
        "risk_action": "NONE",
        "size_scalar": 1.0,
        "detail": payload,
    }


def normalize_tkr7(result: dict[str, object]) -> dict[str, object]:
    payload = result["signal_payload"]
    assert isinstance(payload, dict)
    signal_type = str(payload.get("ao_signal_type", "NONE"))
    recommendation = str(payload.get("ao_recommendation", "STANDBY"))
    if signal_type == "FORCE_EXIT" or recommendation in {"CLOSE", "REDUCE"}:
        direction = "sell"
    elif signal_type == "CONFIRM" and recommendation in {"HOLD", "BUY"}:
        direction = "buy"
    else:
        direction = "neutral"
    return {
        "object_id": "TKR7_P0_E",
        "card_role": "voter",
        "signal_type": signal_type,
        "signal_direction": direction,
        "signal_strength": float(payload.get("ao_signal_strength", 0)),
        "confidence": float(payload.get("ao_divergence_confidence", 0) or 0.5),
        "filter_action": "PASS",
        "risk_action": recommendation,
        "size_scalar": 1.0,
        "detail": payload,
    }


def normalize_voltarget(result: dict[str, object]) -> dict[str, object]:
    payload = result["signal_payload"]
    assert isinstance(payload, dict)
    return {
        "object_id": "VOLTARGET_P0_R",
        "card_role": "sizer",
        "signal_type": "VOL_ADJUST",
        "signal_direction": "neutral",
        "signal_strength": float(payload.get("vt_position_scalar", 1.0)),
        "confidence": 0.7,
        "filter_action": "PASS",
        "risk_action": payload.get("vt_vol_regime", "normal_vol"),
        "size_scalar": float(payload.get("vt_adjusted_position", 1.0)),
        "detail": payload,
    }


def normalize_period_queen(result: dict[str, object]) -> dict[str, object]:
    payload = result["signal_payload"]
    assert isinstance(payload, dict)
    permission = str(payload.get("pq_trading_permission", "REDUCED"))
    filter_action = "PASS"
    if permission == "HALT":
        filter_action = "EXCLUDE"
    elif permission == "EXIT_ONLY":
        filter_action = "REDUCE_WEIGHT"
    return {
        "object_id": "PERIOD_QUEEN_P0_F",
        "card_role": "environment",
        "signal_type": str(payload.get("pq_state", "GESTATION")),
        "signal_direction": "neutral",
        "signal_strength": float(payload.get("pq_state_confidence", 0.5)),
        "confidence": float(payload.get("pq_state_confidence", 0.5)),
        "filter_action": filter_action,
        "risk_action": permission,
        "size_scalar": float(payload.get("pq_position_max_size", 0.0)),
        "detail": payload,
    }


def aggregate(card_results: list[dict[str, object]]) -> dict[str, object]:
    buy_score = 0.0
    sell_score = 0.0
    buy_votes = 0
    sell_votes = 0
    neutral_votes = 0
    blockers: list[str] = []
    hard_block = False
    size_inputs: list[float] = []
    pq_permission = "REDUCED"

    for card in card_results:
        object_id = str(card["object_id"])
        direction = str(card["signal_direction"])
        strength = float(card["signal_strength"])
        confidence = float(card["confidence"])
        filter_action = str(card["filter_action"])
        risk_action = str(card["risk_action"])
        role = str(card["card_role"])

        if role == "voter":
            if direction == "buy":
                buy_votes += 1
                buy_score += strength * confidence
            elif direction == "sell":
                sell_votes += 1
                sell_score += strength * confidence
            else:
                neutral_votes += 1

        if role in {"filter", "sizer"}:
            size_inputs.append(float(card["size_scalar"]))

        if object_id == "PERIOD_QUEEN_P0_F":
            pq_permission = risk_action
            size_inputs.append(float(card["size_scalar"]))

        if filter_action in {"EXCLUDE", "REDUCE_WEIGHT"}:
            blockers.append(object_id)
        if filter_action == "EXCLUDE":
            hard_block = True

    avg_size = sum(size_inputs) / len(size_inputs) if size_inputs else 1.0
    net_score = round(buy_score - sell_score, 6)
    if pq_permission == "HALT" or hard_block:
        final_signal = "NO_TRADE"
    elif net_score >= 2.0:
        final_signal = "BUY"
    elif net_score <= -1.5:
        final_signal = "SELL"
    else:
        final_signal = "NEUTRAL"

    return {
        "buy_votes": buy_votes,
        "sell_votes": sell_votes,
        "neutral_votes": neutral_votes,
        "buy_score": round(buy_score, 6),
        "sell_score": round(sell_score, 6),
        "net_score": net_score,
        "avg_size_scalar": round(avg_size, 6),
        "permission": pq_permission,
        "final_signal": final_signal,
        "blockers": blockers,
    }


def build_vote_input_snapshot(card_results: list[dict[str, object]]) -> list[dict[str, object]]:
    snapshot: list[dict[str, object]] = []
    for card in card_results:
        snapshot.append(
            {
                "object_id": card["object_id"],
                "card_role": card["card_role"],
                "signal_type": card["signal_type"],
                "signal_direction": card["signal_direction"],
                "signal_strength": card["signal_strength"],
                "confidence": card["confidence"],
                "filter_action": card["filter_action"],
                "risk_action": card["risk_action"],
                "size_scalar": card["size_scalar"],
            }
        )
    return snapshot


def build_final_decision_card(summary: dict[str, object]) -> dict[str, object]:
    final_signal = str(summary["final_signal"])
    blockers = list(summary["blockers"])
    permission = str(summary["permission"])
    if final_signal == "NO_TRADE":
        trade_gate = "BLOCKED"
        rationale = "hard_blocker_or_environment_halt"
    elif final_signal == "BUY":
        trade_gate = "ALLOW"
        rationale = "buy_score_dominates_and_no_hard_block"
    elif final_signal == "SELL":
        trade_gate = "EXIT"
        rationale = "sell_score_dominates"
    else:
        trade_gate = "WAIT"
        rationale = "score_not_decisive"
    return {
        "final_signal": final_signal,
        "trade_gate": trade_gate,
        "permission": permission,
        "buy_votes": summary["buy_votes"],
        "sell_votes": summary["sell_votes"],
        "neutral_votes": summary["neutral_votes"],
        "buy_score": summary["buy_score"],
        "sell_score": summary["sell_score"],
        "net_score": summary["net_score"],
        "blockers": blockers,
        "hard_block": bool(blockers and final_signal == "NO_TRADE"),
        "rationale": rationale,
    }


def build_size_policy_card(card_results: list[dict[str, object]], summary: dict[str, object]) -> dict[str, object]:
    pq = next(card for card in card_results if str(card["object_id"]) == "PERIOD_QUEEN_P0_F")
    voltarget = next(card for card in card_results if str(card["object_id"]) == "VOLTARGET_P0_R")
    volfac = next(card for card in card_results if str(card["object_id"]) == "VOLFAC_P0_A")
    pq_size_cap = float(pq["size_scalar"])
    voltarget_size = float(voltarget["size_scalar"])
    filter_scalar = float(volfac["size_scalar"])
    recommended = min(pq_size_cap, voltarget_size) if summary["final_signal"] != "NO_TRADE" else 0.0
    return {
        "environment_cap": pq_size_cap,
        "voltarget_scalar": voltarget_size,
        "volfac_filter_scalar": filter_scalar,
        "avg_size_scalar": summary["avg_size_scalar"],
        "recommended_size_scalar": round(recommended, 6),
        "size_policy": "blocked_to_zero" if summary["final_signal"] == "NO_TRADE" else "min(environment_cap, voltarget_scalar)",
    }


def build_registry_output(input_path: Path, proxy_path: Path, registry_id: str) -> dict[str, object]:
    rows = load_ohlcv_rows(input_path)
    proxy_rows = load_ohlcv_rows(proxy_path)

    volfac = calc_volfac(rows)
    bpb = calc_bpb(rows)
    vp = calc_vp(rows)
    tkr7 = calc_tkr7(rows)
    voltarget = calc_voltarget(rows, target_vol=0.10, base_position=float(volfac["signal_payload"]["size_scalar"]))  # type: ignore[index]
    period_queen = calc_period_queen_proxy(proxy_rows)

    normalized = [
        normalize_volfac(volfac),
        normalize_bpb(bpb),
        normalize_vp(vp),
        normalize_tkr7(tkr7),
        normalize_voltarget(voltarget),
        normalize_period_queen(period_queen),
    ]
    summary = aggregate(normalized)
    return {
        "registry_id": registry_id,
        "input_csv": str(input_path).replace("\\", "/"),
        "market_proxy_csv": str(proxy_path).replace("\\", "/"),
        "as_of_date": rows[-1]["date"],
        "cards_run": [card["object_id"] for card in normalized],
        "vote_input_snapshot": build_vote_input_snapshot(normalized),
        "aggregate_summary": summary,
        "final_decision_card": build_final_decision_card(summary),
        "size_policy_card": build_size_policy_card(normalized, summary),
        "card_results": normalized,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Registry v0: aggregate minimal runnable object cards.")
    parser.add_argument("--input-csv", required=True)
    parser.add_argument("--output-json", required=True)
    parser.add_argument("--market-proxy-csv", help="Optional proxy csv for PERIOD_QUEEN. Defaults to input-csv.")
    parser.add_argument("--registry-id", default="registry_v0_minimal")
    args = parser.parse_args()

    input_path = Path(args.input_csv)
    proxy_path = Path(args.market_proxy_csv) if args.market_proxy_csv else input_path
    payload = build_registry_output(input_path, proxy_path, args.registry_id)

    output = Path(args.output_json)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
