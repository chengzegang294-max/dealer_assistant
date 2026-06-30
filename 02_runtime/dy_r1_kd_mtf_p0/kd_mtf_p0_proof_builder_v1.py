from __future__ import annotations

import argparse
import csv
import json
from bisect import bisect_right
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional


RUNTIME_DIR = Path(__file__).resolve().parent
PARAMS_PATH = RUNTIME_DIR / "kd_mtf_p0_runtime_params_template_v1.json"
UPSTREAM_PATH = RUNTIME_DIR / "upstream_samples" / "n01_first_real_input_bars_v1.csv"
PROOF_INPUT_PATH = RUNTIME_DIR / "real_input_samples" / "kd_mtf_p0_proof_input_v1.csv"
PROOF_OUTPUT_PATH = RUNTIME_DIR / "real_input_samples" / "kd_mtf_p0_proof_output_v1.csv"

PROOF_INPUT_COLUMNS = [
    "symbol",
    "timeframe",
    "bar_time",
    "week_k",
    "week_d",
    "day_k_prev",
    "day_d_prev",
    "day_k",
    "day_d",
    "h4_k",
    "h4_d",
    "input_note",
]

PROOF_OUTPUT_COLUMNS = [
    "symbol",
    "timeframe",
    "bar_time",
    "kd_week_bias",
    "kd_day_signal",
    "kd_4h_confirm",
    "kd_alignment_tier",
    "kd_direction_filter",
    "kd_week_extreme_zone",
    "proof_basis",
]


@dataclass(frozen=True)
class Bar:
    symbol: str
    timeframe: str
    bar_time: datetime
    open: float
    high: float
    low: float
    close: float


@dataclass
class Candle:
    start: datetime
    end: datetime
    open: float
    high: float
    low: float
    close: float
    k: Optional[float] = None
    d: Optional[float] = None


def parse_utc(ts: str) -> datetime:
    return datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def format_utc(ts: datetime) -> str:
    return ts.strftime("%Y-%m-%dT%H:%M:%SZ")


def load_params() -> dict:
    with PARAMS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_h1_bars() -> list[Bar]:
    with UPSTREAM_PATH.open("r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    bars = [
        Bar(
            symbol=row["symbol"],
            timeframe=row["timeframe"],
            bar_time=parse_utc(row["bar_time"]),
            open=float(row["open"]),
            high=float(row["high"]),
            low=float(row["low"]),
            close=float(row["close"]),
        )
        for row in rows
    ]
    assert_h1_contract(bars)
    return bars


def assert_h1_contract(bars: list[Bar]) -> None:
    if not bars:
        raise ValueError("upstream bars are empty")
    symbols = {bar.symbol for bar in bars}
    timeframes = {bar.timeframe for bar in bars}
    if len(symbols) != 1:
        raise ValueError("upstream bars must contain a single symbol")
    if timeframes != {"H1"}:
        raise ValueError("upstream bars must be H1 only")
    times = [bar.bar_time for bar in bars]
    if times != sorted(times):
        raise ValueError("bar_time must be sorted ascending")
    if len(times) != len(set(times)):
        raise ValueError("bar_time must be unique")


def floor_4h(ts: datetime) -> datetime:
    return ts.replace(hour=(ts.hour // 4) * 4, minute=0, second=0, microsecond=0)


def floor_day(ts: datetime) -> datetime:
    return ts.replace(hour=0, minute=0, second=0, microsecond=0)


def floor_week(ts: datetime) -> datetime:
    day_start = floor_day(ts)
    return day_start - timedelta(days=day_start.weekday())


def build_candles(bars: list[Bar], timeframe: str) -> list[Candle]:
    bucket_func = {
        "4h": floor_4h,
        "day": floor_day,
        "week": floor_week,
    }[timeframe]
    duration = {
        "4h": timedelta(hours=4),
        "day": timedelta(days=1),
        "week": timedelta(days=7),
    }[timeframe]
    grouped: list[Candle] = []
    current_start: Optional[datetime] = None
    current_bars: list[Bar] = []
    for bar in bars:
        bucket_start = bucket_func(bar.bar_time)
        if current_start is None or bucket_start != current_start:
            if current_bars:
                grouped.append(candle_from_bars(current_start, duration, current_bars))
            current_start = bucket_start
            current_bars = [bar]
        else:
            current_bars.append(bar)
    if current_bars and current_start is not None:
        grouped.append(candle_from_bars(current_start, duration, current_bars))
    return grouped


def candle_from_bars(start: datetime, duration: timedelta, bars: list[Bar]) -> Candle:
    return Candle(
        start=start,
        end=start + duration,
        open=bars[0].open,
        high=max(bar.high for bar in bars),
        low=min(bar.low for bar in bars),
        close=bars[-1].close,
    )


def rolling_sma(values: list[Optional[float]], window: int) -> list[Optional[float]]:
    result: list[Optional[float]] = []
    for index in range(len(values)):
        if index + 1 < window:
            result.append(None)
            continue
        chunk = values[index - window + 1 : index + 1]
        if any(value is None for value in chunk):
            result.append(None)
            continue
        numeric_chunk = [value for value in chunk if value is not None]
        result.append(sum(numeric_chunk) / window)
    return result


def compute_stochastic(candles: list[Candle], length: int, smooth_k: int, smooth_d: int) -> None:
    raw_k: list[Optional[float]] = []
    for index, candle in enumerate(candles):
        if index + 1 < length:
            raw_k.append(None)
            continue
        window = candles[index - length + 1 : index + 1]
        highest_high = max(item.high for item in window)
        lowest_low = min(item.low for item in window)
        if highest_high == lowest_low:
            raw_k.append(None)
            continue
        raw_k.append(100.0 * (candle.close - lowest_low) / (highest_high - lowest_low))
    smooth_k_values = rolling_sma(raw_k, smooth_k)
    smooth_d_values = rolling_sma(smooth_k_values, smooth_d)
    for candle, k_value, d_value in zip(candles, smooth_k_values, smooth_d_values):
        candle.k = k_value
        candle.d = d_value


def load_target_times() -> list[datetime]:
    preferred_path = PROOF_OUTPUT_PATH if PROOF_OUTPUT_PATH.exists() else PROOF_INPUT_PATH
    with preferred_path.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError("existing proof file has no target rows")
    return [parse_utc(row["bar_time"]) for row in rows]


def normalize_target_times(raw_values: list[str]) -> list[datetime]:
    targets: list[datetime] = []
    for raw_value in raw_values:
        for part in raw_value.split(","):
            candidate = part.strip()
            if candidate:
                targets.append(parse_utc(candidate))
    if not targets:
        raise ValueError("custom target list is empty")
    if len(targets) != len(set(targets)):
        raise ValueError("custom target list contains duplicate bar_time values")
    if targets != sorted(targets):
        raise ValueError("custom target list must be sorted ascending")
    return targets


def assert_target_times_exist(bars: list[Bar], target_times: list[datetime]) -> None:
    bar_times = {bar.bar_time for bar in bars}
    missing = [format_utc(target_time) for target_time in target_times if target_time not in bar_times]
    if missing:
        raise ValueError("target bar_time not found in upstream H1 bars: {0}".format(", ".join(missing)))


def last_closed_index(candles: list[Candle], target_time: datetime) -> Optional[int]:
    ends = [candle.end for candle in candles]
    index = bisect_right(ends, target_time) - 1
    return index if index >= 0 else None


def fmt_float(value: Optional[float]) -> str:
    return "" if value is None else f"{value:.6f}"


def resolve_h4_tie_epsilon(params: dict, override: Optional[float]) -> float:
    if override is not None:
        return float(override)
    raw = params.get("kd_config", {}).get("h4_confirm_tie_epsilon", 0.0)
    return float(raw)



def derive_week_bias(week_k: Optional[float], week_d: Optional[float]) -> str:
    if week_k is None or week_d is None:
        return "unknown"
    if week_k > week_d:
        return "up"
    if week_k < week_d:
        return "down"
    return "unknown"


def derive_day_signal(
    day_k_prev: Optional[float],
    day_d_prev: Optional[float],
    day_k: Optional[float],
    day_d: Optional[float],
) -> str:
    if None in (day_k_prev, day_d_prev, day_k, day_d):
        return "unknown"
    if day_k_prev <= day_d_prev and day_k > day_d:
        return "golden_cross"
    if day_k_prev >= day_d_prev and day_k < day_d:
        return "death_cross"
    return "none"


def derive_h4_confirm(h4_k: Optional[float], h4_d: Optional[float], tie_epsilon: float) -> str:
    if h4_k is None or h4_d is None:
        return "unknown"
    if tie_epsilon > 0 and abs(h4_k - h4_d) <= tie_epsilon:
        return "none"
    if h4_k > h4_d:
        return "confirm_up"
    if h4_k < h4_d:
        return "confirm_down"
    return "none"


def derive_alignment_tier(week_bias: str, day_signal: str, h4_confirm: str) -> str:
    if day_signal in {"unknown", "none"} or h4_confirm == "unknown":
        return "unknown"
    if h4_confirm == "none":
        return "b"
    if day_signal == "golden_cross":
        if h4_confirm == "confirm_up":
            if week_bias == "up":
                return "s"
            if week_bias == "unknown":
                return "a"
            return "conflict"
        return "conflict"
    if day_signal == "death_cross":
        if h4_confirm == "confirm_down":
            if week_bias == "down":
                return "s"
            if week_bias == "unknown":
                return "a"
            return "conflict"
        return "conflict"
    return "unknown"


def derive_direction_filter(day_signal: str, tier: str) -> str:
    if tier in {"s", "a"}:
        if day_signal == "golden_cross":
            return "long_preferred"
        if day_signal == "death_cross":
            return "short_preferred"
    if tier in {"b", "conflict"}:
        return "wait"
    return "unknown"


def derive_week_zone(week_k: Optional[float], week_d: Optional[float], low: float, high: float) -> str:
    if week_k is None or week_d is None:
        return "unknown"
    if week_k >= high and week_d >= high:
        return "overbought"
    if week_k <= low and week_d <= low:
        return "oversold"
    return "normal"


def derive_note(day_signal: str, tier: str, week_bias: str) -> str:
    if tier in {"s", "a", "b"}:
        direction = "up" if day_signal == "golden_cross" else "down" if day_signal == "death_cross" else "unknown"
        note = f"real_{tier}_{direction}_from_n01_h1"
    elif tier == "conflict":
        note = "real_conflict_from_n01_h1"
    else:
        note = "real_unknown_from_n01_h1"
    if week_bias == "unknown":
        note += "__week_unknown_utc_closed_buckets_v1"
    else:
        note += "__utc_closed_buckets_v1"
    return note


def build_rows(
    params: dict,
    explicit_target_times: Optional[list[datetime]] = None,
    tie_epsilon: float = 0.0,
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    bars = load_h1_bars()
    target_times = explicit_target_times if explicit_target_times is not None else load_target_times()
    assert_target_times_exist(bars, target_times)
    four_hour = build_candles(bars, "4h")
    daily = build_candles(bars, "day")
    weekly = build_candles(bars, "week")
    compute_stochastic(
        four_hour,
        params["kd_config"]["kd_length"],
        params["kd_config"]["kd_smooth_k"],
        params["kd_config"]["kd_smooth_d"],
    )
    compute_stochastic(
        daily,
        params["kd_config"]["kd_length"],
        params["kd_config"]["kd_smooth_k"],
        params["kd_config"]["kd_smooth_d"],
    )
    compute_stochastic(
        weekly,
        params["kd_config"]["kd_length"],
        params["kd_config"]["kd_smooth_k"],
        params["kd_config"]["kd_smooth_d"],
    )

    symbol = bars[0].symbol
    timeframe = bars[0].timeframe
    proof_input_rows: list[dict[str, str]] = []
    proof_output_rows: list[dict[str, str]] = []

    for target_time in target_times:
        week_index = last_closed_index(weekly, target_time)
        day_index = last_closed_index(daily, target_time)
        h4_index = last_closed_index(four_hour, target_time)

        week_candle = weekly[week_index] if week_index is not None else None
        day_candle = daily[day_index] if day_index is not None else None
        day_prev = daily[day_index - 1] if day_index is not None and day_index - 1 >= 0 else None
        h4_candle = four_hour[h4_index] if h4_index is not None else None

        week_k = week_candle.k if week_candle else None
        week_d = week_candle.d if week_candle else None
        day_k_prev = day_prev.k if day_prev else None
        day_d_prev = day_prev.d if day_prev else None
        day_k = day_candle.k if day_candle else None
        day_d = day_candle.d if day_candle else None
        h4_k = h4_candle.k if h4_candle else None
        h4_d = h4_candle.d if h4_candle else None

        week_bias = derive_week_bias(week_k, week_d)
        day_signal = derive_day_signal(day_k_prev, day_d_prev, day_k, day_d)
        h4_confirm = derive_h4_confirm(h4_k, h4_d, tie_epsilon)
        tier = derive_alignment_tier(week_bias, day_signal, h4_confirm)
        direction_filter = derive_direction_filter(day_signal, tier)
        week_zone = derive_week_zone(
            week_k,
            week_d,
            params["kd_config"]["week_extreme_low"],
            params["kd_config"]["week_extreme_high"],
        )
        note = derive_note(day_signal, tier, week_bias)

        proof_input_rows.append(
            {
                "symbol": symbol,
                "timeframe": timeframe,
                "bar_time": format_utc(target_time),
                "week_k": fmt_float(week_k),
                "week_d": fmt_float(week_d),
                "day_k_prev": fmt_float(day_k_prev),
                "day_d_prev": fmt_float(day_d_prev),
                "day_k": fmt_float(day_k),
                "day_d": fmt_float(day_d),
                "h4_k": fmt_float(h4_k),
                "h4_d": fmt_float(h4_d),
                "input_note": note,
            }
        )
        proof_output_rows.append(
            {
                "symbol": symbol,
                "timeframe": timeframe,
                "bar_time": format_utc(target_time),
                "kd_week_bias": week_bias,
                "kd_day_signal": day_signal,
                "kd_4h_confirm": h4_confirm,
                "kd_alignment_tier": tier,
                "kd_direction_filter": direction_filter,
                "kd_week_extreme_zone": week_zone,
                "proof_basis": note,
            }
        )

    return proof_input_rows, proof_output_rows


def scan_tiers(params: dict, tie_epsilon: float) -> tuple[dict[str, int], list[datetime]]:
    bars = load_h1_bars()
    four_hour = build_candles(bars, "4h")
    daily = build_candles(bars, "day")
    weekly = build_candles(bars, "week")
    compute_stochastic(
        four_hour,
        params["kd_config"]["kd_length"],
        params["kd_config"]["kd_smooth_k"],
        params["kd_config"]["kd_smooth_d"],
    )
    compute_stochastic(
        daily,
        params["kd_config"]["kd_length"],
        params["kd_config"]["kd_smooth_k"],
        params["kd_config"]["kd_smooth_d"],
    )
    compute_stochastic(
        weekly,
        params["kd_config"]["kd_length"],
        params["kd_config"]["kd_smooth_k"],
        params["kd_config"]["kd_smooth_d"],
    )

    counts: dict[str, int] = {}
    b_candidates: list[datetime] = []

    for bar in bars:
        target_time = bar.bar_time
        week_index = last_closed_index(weekly, target_time)
        day_index = last_closed_index(daily, target_time)
        h4_index = last_closed_index(four_hour, target_time)

        week_candle = weekly[week_index] if week_index is not None else None
        day_candle = daily[day_index] if day_index is not None else None
        day_prev = daily[day_index - 1] if day_index is not None and day_index - 1 >= 0 else None
        h4_candle = four_hour[h4_index] if h4_index is not None else None

        week_k = week_candle.k if week_candle else None
        week_d = week_candle.d if week_candle else None
        day_k_prev = day_prev.k if day_prev else None
        day_d_prev = day_prev.d if day_prev else None
        day_k = day_candle.k if day_candle else None
        day_d = day_candle.d if day_candle else None
        h4_k = h4_candle.k if h4_candle else None
        h4_d = h4_candle.d if h4_candle else None

        week_bias = derive_week_bias(week_k, week_d)
        day_signal = derive_day_signal(day_k_prev, day_d_prev, day_k, day_d)
        h4_confirm = derive_h4_confirm(h4_k, h4_d, tie_epsilon)
        tier = derive_alignment_tier(week_bias, day_signal, h4_confirm)

        counts[tier] = counts.get(tier, 0) + 1
        if tier == "b":
            b_candidates.append(target_time)

    return counts, b_candidates


def extend_targets_with_first_b(
    params: dict,
    tie_epsilon: float,
) -> tuple[list[datetime], Optional[datetime], dict[str, int], int]:
    existing = load_target_times()
    existing_set = set(existing)
    counts, candidates = scan_tiers(params, tie_epsilon)
    for candidate in candidates:
        if candidate not in existing_set:
            extended = sorted(existing + [candidate])
            return extended, candidate, counts, len(candidates)
    return existing, None, counts, len(candidates)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def rows_equal(expected: list[dict[str, str]], actual: list[dict[str, str]]) -> bool:
    return expected == actual


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--persist",
        action="store_true",
        help="write generated proof_input/proof_output back to local runtime directory",
    )
    parser.add_argument(
        "--scan-b",
        action="store_true",
        help="scan all upstream H1 bar_time values and list b-tier candidates under current tie epsilon",
    )
    parser.add_argument(
        "--scan-limit",
        type=int,
        default=20,
        help="limit number of scan candidates printed for b-tier",
    )
    parser.add_argument(
        "--extend-proof-with-first-b",
        action="store_true",
        help="extend existing proof targets by adding the first b-tier candidate not already present",
    )
    parser.add_argument(
        "--override-h4-confirm-tie-epsilon",
        type=float,
        default=None,
        help="override kd_config.h4_confirm_tie_epsilon for this run",
    )
    parser.add_argument(
        "--target-bar-time",
        action="append",
        default=[],
        help="one or more explicit H1 target bar_time values in UTC ISO8601, supports repeated flags or comma-separated list",
    )
    args = parser.parse_args()

    params = load_params()
    tie_epsilon = resolve_h4_tie_epsilon(params, args.override_h4_confirm_tie_epsilon)
    if args.extend_proof_with_first_b:
        explicit_target_times, added, scan_counts, scan_candidate_count = extend_targets_with_first_b(
            params,
            tie_epsilon,
        )
    else:
        explicit_target_times = normalize_target_times(args.target_bar_time) if args.target_bar_time else None
        added = None
        scan_counts = {}
        scan_candidate_count = 0

    if args.scan_b:
        scan_counts, scan_candidates = scan_tiers(params, tie_epsilon)
    else:
        scan_candidates = []

    proof_input_rows, proof_output_rows = build_rows(
        params,
        explicit_target_times=explicit_target_times,
        tie_epsilon=tie_epsilon,
    )
    existing_input_rows = read_csv_rows(PROOF_INPUT_PATH) if PROOF_INPUT_PATH.exists() else []
    existing_output_rows = read_csv_rows(PROOF_OUTPUT_PATH) if PROOF_OUTPUT_PATH.exists() else []

    print("builder_mode={0}".format("persist" if args.persist else "dry_run"))
    print("upstream_path={0}".format(UPSTREAM_PATH))
    print("h4_confirm_tie_epsilon={0}".format(tie_epsilon))
    if args.scan_b:
        print("scan_total_b_candidates={0}".format(len(scan_candidates)))
        print("scan_tier_counts={0}".format(json.dumps(scan_counts, ensure_ascii=True, sort_keys=True)))
        if scan_candidates:
            preview = scan_candidates[: max(0, args.scan_limit)]
            print("scan_b_candidates_preview={0}".format(",".join(format_utc(ts) for ts in preview)))
    if args.extend_proof_with_first_b:
        print("extend_added_b_target={0}".format(format_utc(added) if added else ""))
        print("extend_scan_total_b_candidates={0}".format(scan_candidate_count))
        print("extend_scan_tier_counts={0}".format(json.dumps(scan_counts, ensure_ascii=True, sort_keys=True)))
    print(
        "target_source={0}".format(
            "custom_args" if explicit_target_times is not None else "existing_proof_files"
        )
    )
    print("target_row_count={0}".format(len(proof_input_rows)))
    print("proof_input_matches_existing={0}".format(rows_equal(proof_input_rows, existing_input_rows)).lower())
    print("proof_output_matches_existing={0}".format(rows_equal(proof_output_rows, existing_output_rows)).lower())
    if proof_input_rows:
        print("first_target={0}".format(proof_input_rows[0]["bar_time"]))
        print("last_target={0}".format(proof_input_rows[-1]["bar_time"]))
        print("first_output_row={0}".format(json.dumps(proof_output_rows[0], ensure_ascii=True)))

    if args.persist:
        write_csv(PROOF_INPUT_PATH, PROOF_INPUT_COLUMNS, proof_input_rows)
        write_csv(PROOF_OUTPUT_PATH, PROOF_OUTPUT_COLUMNS, proof_output_rows)
        print("persisted_proof_input={0}".format(PROOF_INPUT_PATH))
        print("persisted_proof_output={0}".format(PROOF_OUTPUT_PATH))
    else:
        print("dry_run_only=true")


if __name__ == "__main__":
    main()
