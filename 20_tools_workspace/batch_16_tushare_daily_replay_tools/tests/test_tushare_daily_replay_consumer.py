from __future__ import annotations

import hashlib
import importlib.util
import json
import csv
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parent.parent / "tushare_daily_replay_consumer.py"
SPEC = importlib.util.spec_from_file_location("tushare_daily_replay_consumer", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ReplayConsumerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.snapshot_root = self.root / "snapshots"
        self.snapshot_root.mkdir(parents=True, exist_ok=True)
        self.manifest_path = self.root / "manifest.json"

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _sha256_text(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def _sha256_file(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    def _rewrite_snapshot_and_manifest_entry(
        self,
        *,
        path: Path,
        entry: dict[str, object],
        snapshot: dict[str, object],
    ) -> None:
        response_payload = snapshot["source_response_json"]
        snapshot["source_response_text"] = json.dumps(
            response_payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        snapshot["source_response_sha256"] = self._sha256_text(snapshot["source_response_text"])
        data_block = response_payload["data"]
        snapshot["fields"] = data_block["fields"]
        snapshot["row_count"] = len(data_block["items"])
        path.write_text(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        entry["field_list"] = snapshot["fields"]
        entry["row_count"] = snapshot["row_count"]
        entry["source_response_sha256"] = snapshot["source_response_sha256"]
        entry["snapshot_file_sha256"] = self._sha256_file(path)

    def _write_snapshot(
        self,
        *,
        manifest_key: str,
        api_name: str,
        file_name: str,
        capture_time_utc: str,
        fields: list[str],
        items: list[list[object]],
        params: dict[str, object] | None = None,
    ) -> dict[str, object]:
        response_payload = {
            "code": 0,
            "message": "",
            "data": {
                "fields": fields,
                "items": items,
                "has_more": False,
                "count": 0,
            },
            "request_id": "synthetic",
            "chart": None,
        }
        source_response_text = json.dumps(
            response_payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )
        source_response_sha256 = self._sha256_text(source_response_text)
        snapshot_payload = {
            "snapshot_id": manifest_key,
            "snapshot_role": "DERIVED_PAGE_AGGREGATE",
            "source_response_origin": "DERIVED_PAGE_AGGREGATE_NOT_VENDOR_RAW",
            "api_name": api_name,
            "capture_time_utc": capture_time_utc,
            "http_status": 200,
            "request_meta_redacted": {
                "doc_id": "synthetic",
                "params": params or {},
                "fields": fields,
            },
            "params": params or {},
            "fields": fields,
            "row_count": len(items),
            "source_response_text": source_response_text,
            "source_response_sha256": source_response_sha256,
            "source_response_json": response_payload,
            "derived_from_page_responses": [
                {
                    "page_index": 1,
                    "raw_page_path": f"raw_pages/{manifest_key}/page_0001.json",
                    "capture_time_utc": capture_time_utc,
                    "source_response_sha256": source_response_sha256,
                    "snapshot_file_sha256": "raw_page_file_sha256_placeholder",
                    "row_count": len(items),
                    "field_list": fields,
                }
            ],
        }
        path = self.snapshot_root / file_name
        path.write_text(json.dumps(snapshot_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return {
            "manifest_key": manifest_key,
            "source_id": MODULE.EXPECTED_SOURCE_ID,
            "snapshot_path": file_name,
            "api_name": api_name,
            "capture_time_utc": capture_time_utc,
            "source_response_sha256": source_response_sha256,
            "snapshot_file_sha256": self._sha256_file(path),
            "row_count": len(items),
            "field_list": fields,
            "scope": "synthetic_test_scope",
            "status": "ready",
        }

    def _base_entries(self) -> list[dict[str, object]]:
        stock_basic_entry = self._write_snapshot(
            manifest_key="stock_basic_active",
            api_name="stock_basic",
            file_name="stock_basic_active.json",
            capture_time_utc="2026-09-01T08:56:43.808Z",
            fields=[
                "ts_code",
                "symbol",
                "market",
                "exchange",
                "list_status",
                "list_date",
                "delist_date",
            ],
            items=[
                ["600000.SH", "600000", "主板", "SSE", "L", "19991110", None],
                ["000001.SZ", "000001", "主板", "SZSE", "L", "19910403", None],
                ["430001.BJ", "430001", "北交所", "BSE", "L", "20200101", None],
            ],
            params={"list_status": "L"},
        )
        trade_cal_sse_entry = self._write_snapshot(
            manifest_key="trade_cal_sse",
            api_name="trade_cal",
            file_name="trade_cal_sse.json",
            capture_time_utc="2026-09-01T08:56:51.719Z",
            fields=["exchange", "cal_date", "is_open", "pretrade_date"],
            items=[
                ["SSE", "20260902", 1, "20260901"],
                ["SSE", "20260901", 1, "20260831"],
                ["SSE", "20260831", 1, "20260828"],
            ],
            params={"exchange": "SSE"},
        )
        trade_cal_szse_entry = self._write_snapshot(
            manifest_key="trade_cal_szse",
            api_name="trade_cal",
            file_name="trade_cal_szse.json",
            capture_time_utc="2026-09-01T08:56:57.342Z",
            fields=["exchange", "cal_date", "is_open", "pretrade_date"],
            items=[
                ["SZSE", "20260902", 1, "20260901"],
                ["SZSE", "20260901", 1, "20260831"],
                ["SZSE", "20260831", 1, "20260828"],
            ],
            params={"exchange": "SZSE"},
        )
        daily_entry = self._write_snapshot(
            manifest_key="daily_all_market",
            api_name="daily",
            file_name="daily_all_market.json",
            capture_time_utc="2026-09-01T06:51:04.364Z",
            fields=[
                "ts_code",
                "trade_date",
                "open",
                "high",
                "low",
                "close",
                "pre_close",
                "change",
                "pct_chg",
                "vol",
                "amount",
            ],
            items=[
                ["600000.SH", "20260831", 10.0, 10.2, 9.9, 10.1, 10.0, 0.1, 1.0, 5000, 8000],
                ["000001.SZ", "20260831", 12.0, 12.3, 11.8, 12.1, 12.0, 0.1, 0.8333, 3000, 4000],
                ["430001.BJ", "20260831", 8.0, 8.2, 7.9, 8.1, 8.0, 0.1, 1.25, 1000, 2000],
            ],
            params={"trade_date": "20260831"},
        )
        adj_factor_entry = self._write_snapshot(
            manifest_key="adj_factor_all_market",
            api_name="adj_factor",
            file_name="adj_factor_all_market.json",
            capture_time_utc="2026-09-01T06:50:28.863Z",
            fields=["ts_code", "trade_date", "adj_factor"],
            items=[
                ["600000.SH", "20260831", 1.0],
                ["000001.SZ", "20260831", 2.0],
                ["430001.BJ", "20260831", 3.0],
            ],
            params={"trade_date": "20260831"},
        )
        return [
            stock_basic_entry,
            trade_cal_sse_entry,
            trade_cal_szse_entry,
            daily_entry,
            adj_factor_entry,
        ]

    def _write_manifest(self, entries: list[dict[str, object]]) -> None:
        self.manifest_path.write_text(
            json.dumps({"run_status": "SUCCESS", "entries": entries}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _build_success_result(self) -> MODULE.ReplayResult:
        entries = self._base_entries()
        self._write_manifest(entries)
        return MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)

    def test_sse_szse_success_and_bse_exclusion(self) -> None:
        result = self._build_success_result()
        self.assertEqual(result.summary["status"], "SUCCESS")
        self.assertEqual(result.summary["normalized_output_row_count"], 2)
        self.assertEqual(result.summary["bse_exclusion_count"], 1)
        self.assertEqual(result.quality_report["run_status"], "SUCCESS")
        self.assertEqual(result.summary["latest_complete_trade_date_by_exchange"]["SSE"], "20260831")
        self.assertEqual(result.summary["latest_complete_trade_date_by_exchange"]["SZSE"], "20260831")
        self.assertEqual(result.quality_report["passed_row_count"], 2)
        self.assertEqual(result.quality_report["out_of_scope_exclusion_row_count"], 2)
        self.assertEqual(result.quality_report["quality_exclusion_row_count"], 0)
        self.assertEqual(result.quality_report["quality_failed_row_count"], 0)

        ts_codes = {row["ts_code"] for row in result.normalized_rows}
        self.assertEqual(ts_codes, {"600000.SH", "000001.SZ"})
        self.assertEqual(result.quality_report["exclusion_reason_counts"]["BSE_EXCLUDED_BY_FORMAL_SCOPE"], 1)

    def test_source_response_sha_mismatch_raises(self) -> None:
        entries = self._base_entries()
        entries[0]["source_response_sha256"] = "0" * 64
        self._write_manifest(entries)
        with self.assertRaises(MODULE.ReplayValidationError):
            MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)

    def test_snapshot_file_sha_mismatch_raises(self) -> None:
        entries = self._base_entries()
        entries[0]["snapshot_file_sha256"] = "1" * 64
        self._write_manifest(entries)
        with self.assertRaises(MODULE.ReplayValidationError):
            MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)

    def test_manifest_required_field_missing_raises(self) -> None:
        entries = self._base_entries()
        del entries[0]["field_list"]
        self._write_manifest(entries)
        with self.assertRaises(MODULE.ReplayValidationError):
            MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)

    def test_missing_run_status_is_rejected(self) -> None:
        entries = self._base_entries()
        self.manifest_path.write_text(
            json.dumps({"entries": entries}, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        with self.assertRaises(MODULE.ReplayValidationError) as ctx:
            MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)
        self.assertIn("run_status must be SUCCESS", str(ctx.exception))

    def test_required_field_missing_raises(self) -> None:
        entries = self._base_entries()
        daily_path = self.snapshot_root / "daily_all_market.json"
        snapshot = json.loads(daily_path.read_text(encoding="utf-8"))
        snapshot["source_response_json"]["data"]["fields"] = [
            field for field in snapshot["source_response_json"]["data"]["fields"] if field != "amount"
        ]
        self._rewrite_snapshot_and_manifest_entry(path=daily_path, entry=entries[3], snapshot=snapshot)
        self._write_manifest(entries)
        with self.assertRaises(MODULE.ReplayValidationError):
            MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)

    def test_daily_without_stock_basic_match_blocks(self) -> None:
        entries = self._base_entries()
        daily_path = self.snapshot_root / "daily_all_market.json"
        snapshot = json.loads(daily_path.read_text(encoding="utf-8"))
        snapshot["source_response_json"]["data"]["items"].append(
            ["300999.SZ", "20260831", 20.0, 20.5, 19.8, 20.2, 20.0, 0.2, 1.0, 2000, 3500]
        )
        self._rewrite_snapshot_and_manifest_entry(path=daily_path, entry=entries[3], snapshot=snapshot)
        self._write_manifest(entries)

        with self.assertRaises(MODULE.ReplayValidationError) as ctx:
            MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)
        self.assertIn("daily rows exist that cannot join to active stock_basic", str(ctx.exception))

    def test_daily_matching_non_l_stock_basic_blocks(self) -> None:
        entries = self._base_entries()
        stock_path = self.snapshot_root / "stock_basic_active.json"
        snapshot = json.loads(stock_path.read_text(encoding="utf-8"))
        snapshot["source_response_json"]["data"]["items"][0] = [
            "600000.SH",
            "600000",
            "主板",
            "SSE",
            "D",
            "19991110",
            "20260830",
        ]
        self._rewrite_snapshot_and_manifest_entry(path=stock_path, entry=entries[0], snapshot=snapshot)
        self._write_manifest(entries)

        with self.assertRaises(MODULE.ReplayValidationError) as ctx:
            MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)
        self.assertIn("daily rows exist that cannot join to active stock_basic", str(ctx.exception))

    def test_raw_and_future_derived_fields_stay_separate(self) -> None:
        result = self._build_success_result()
        output_columns = set(result.normalized_rows[0].keys())

        self.assertIn("open", output_columns)
        self.assertIn("adj_factor", output_columns)
        self.assertNotIn("qfq_close_end_date_bound", output_columns)
        self.assertNotIn("hfq_close", output_columns)
        self.assertNotIn("turnover_rate", output_columns)
        self.assertNotIn("sma5", output_columns)

    def test_provenance_fields_flow_to_final_rows(self) -> None:
        result = self._build_success_result()
        normalized_row = result.normalized_rows[0]
        exclusion_row = result.exclusion_rows[0]
        self.assertEqual(normalized_row["snapshot_role"], "DERIVED_PAGE_AGGREGATE")
        self.assertEqual(
            normalized_row["source_response_origin"],
            "DERIVED_PAGE_AGGREGATE_NOT_VENDOR_RAW",
        )
        self.assertEqual(exclusion_row["snapshot_role"], "DERIVED_PAGE_AGGREGATE")
        self.assertEqual(
            exclusion_row["source_response_origin"],
            "DERIVED_PAGE_AGGREGATE_NOT_VENDOR_RAW",
        )

    def test_written_tsvs_carry_provenance_columns(self) -> None:
        result = self._build_success_result()
        output_dir = self.root / "output"
        MODULE.write_success_outputs(output_dir, result)

        with (output_dir / "normalized_daily_output.tsv").open(encoding="utf-8", newline="") as handle:
            normalized_rows = list(csv.DictReader(handle, delimiter="\t"))
        with (output_dir / "exclusion_register.tsv").open(encoding="utf-8", newline="") as handle:
            exclusion_rows = list(csv.DictReader(handle, delimiter="\t"))

        self.assertEqual(normalized_rows[0]["snapshot_role"], "DERIVED_PAGE_AGGREGATE")
        self.assertEqual(
            normalized_rows[0]["source_response_origin"],
            "DERIVED_PAGE_AGGREGATE_NOT_VENDOR_RAW",
        )
        self.assertEqual(exclusion_rows[0]["snapshot_role"], "DERIVED_PAGE_AGGREGATE")
        self.assertEqual(
            exclusion_rows[0]["source_response_origin"],
            "DERIVED_PAGE_AGGREGATE_NOT_VENDOR_RAW",
        )

    def test_daily_primary_key_duplicate_blocks(self) -> None:
        entries = self._base_entries()
        daily_path = self.snapshot_root / "daily_all_market.json"
        snapshot = json.loads(daily_path.read_text(encoding="utf-8"))
        duplicate_row = snapshot["source_response_json"]["data"]["items"][0]
        snapshot["source_response_json"]["data"]["items"].append(duplicate_row)
        self._rewrite_snapshot_and_manifest_entry(path=daily_path, entry=entries[3], snapshot=snapshot)
        self._write_manifest(entries)

        with self.assertRaises(MODULE.ReplayValidationError) as ctx:
            MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)
        self.assertIn("daily contains duplicate", str(ctx.exception))

    def test_adj_factor_primary_key_duplicate_blocks(self) -> None:
        entries = self._base_entries()
        adj_path = self.snapshot_root / "adj_factor_all_market.json"
        snapshot = json.loads(adj_path.read_text(encoding="utf-8"))
        duplicate_row = snapshot["source_response_json"]["data"]["items"][0]
        snapshot["source_response_json"]["data"]["items"].append(duplicate_row)
        self._rewrite_snapshot_and_manifest_entry(path=adj_path, entry=entries[4], snapshot=snapshot)
        self._write_manifest(entries)

        with self.assertRaises(MODULE.ReplayValidationError) as ctx:
            MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)
        self.assertIn("adj_factor contains duplicate", str(ctx.exception))

    def test_stock_basic_ts_code_duplicate_blocks(self) -> None:
        entries = self._base_entries()
        stock_path = self.snapshot_root / "stock_basic_active.json"
        snapshot = json.loads(stock_path.read_text(encoding="utf-8"))
        duplicate_row = snapshot["source_response_json"]["data"]["items"][0]
        snapshot["source_response_json"]["data"]["items"].append(duplicate_row)
        self._rewrite_snapshot_and_manifest_entry(path=stock_path, entry=entries[0], snapshot=snapshot)
        self._write_manifest(entries)

        with self.assertRaises(MODULE.ReplayValidationError) as ctx:
            MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)
        self.assertIn("stock_basic contains duplicate", str(ctx.exception))

    def test_invalid_ohlc_row_is_excluded(self) -> None:
        entries = self._base_entries()
        daily_path = self.snapshot_root / "daily_all_market.json"
        snapshot = json.loads(daily_path.read_text(encoding="utf-8"))
        snapshot["source_response_json"]["data"]["items"][0] = [
            "600000.SH",
            "20260831",
            10.0,
            9.0,
            9.9,
            10.1,
            10.0,
            0.1,
            1.0,
            5000,
            8000,
        ]
        self._rewrite_snapshot_and_manifest_entry(path=daily_path, entry=entries[3], snapshot=snapshot)
        self._write_manifest(entries)

        result = MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)
        reasons = result.quality_report["exclusion_reason_counts"]
        self.assertEqual(result.summary["normalized_output_row_count"], 1)
        self.assertIn("OHLC_HIGH_RELATION_INVALID", reasons)

    def test_negative_volume_or_amount_is_excluded(self) -> None:
        entries = self._base_entries()
        daily_path = self.snapshot_root / "daily_all_market.json"
        snapshot = json.loads(daily_path.read_text(encoding="utf-8"))
        snapshot["source_response_json"]["data"]["items"][0][9] = -1
        snapshot["source_response_json"]["data"]["items"][1][10] = -5
        self._rewrite_snapshot_and_manifest_entry(path=daily_path, entry=entries[3], snapshot=snapshot)
        self._write_manifest(entries)

        result = MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)
        reasons = result.quality_report["exclusion_reason_counts"]
        self.assertIn("VOL_NEGATIVE", reasons)
        self.assertIn("AMOUNT_NEGATIVE", reasons)
        self.assertEqual(result.summary["normalized_output_row_count"], 0)

    def test_pct_chg_outside_tolerance_is_excluded(self) -> None:
        entries = self._base_entries()
        daily_path = self.snapshot_root / "daily_all_market.json"
        snapshot = json.loads(daily_path.read_text(encoding="utf-8"))
        snapshot["source_response_json"]["data"]["items"][0][8] = 2.0
        self._rewrite_snapshot_and_manifest_entry(path=daily_path, entry=entries[3], snapshot=snapshot)
        self._write_manifest(entries)

        result = MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)
        self.assertIn("PCT_CHG_MISMATCH_EXCEEDS_TOLERANCE", result.quality_report["exclusion_reason_counts"])

    def test_change_outside_tolerance_is_excluded(self) -> None:
        entries = self._base_entries()
        daily_path = self.snapshot_root / "daily_all_market.json"
        snapshot = json.loads(daily_path.read_text(encoding="utf-8"))
        snapshot["source_response_json"]["data"]["items"][0][6] = 10.0
        snapshot["source_response_json"]["data"]["items"][0][7] = 0.5
        self._rewrite_snapshot_and_manifest_entry(path=daily_path, entry=entries[3], snapshot=snapshot)
        self._write_manifest(entries)

        result = MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)
        self.assertIn("CHANGE_MISMATCH_EXCEEDS_TOLERANCE", result.quality_report["exclusion_reason_counts"])

    def test_adj_factor_not_positive_is_excluded(self) -> None:
        entries = self._base_entries()
        adj_path = self.snapshot_root / "adj_factor_all_market.json"
        snapshot = json.loads(adj_path.read_text(encoding="utf-8"))
        snapshot["source_response_json"]["data"]["items"][0][2] = 0
        self._rewrite_snapshot_and_manifest_entry(path=adj_path, entry=entries[4], snapshot=snapshot)
        self._write_manifest(entries)

        result = MODULE.consume_snapshots(self.manifest_path, self.snapshot_root)
        self.assertIn("ADJ_FACTOR_NOT_POSITIVE", result.quality_report["exclusion_reason_counts"])


if __name__ == "__main__":
    unittest.main()
