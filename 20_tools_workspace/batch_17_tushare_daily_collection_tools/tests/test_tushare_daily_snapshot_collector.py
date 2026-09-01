from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path


COLLECTOR_PATH = Path(__file__).resolve().parent.parent / "tushare_daily_snapshot_collector.py"
COLLECTOR_SPEC = importlib.util.spec_from_file_location(
    "tushare_daily_snapshot_collector", COLLECTOR_PATH
)
COLLECTOR = importlib.util.module_from_spec(COLLECTOR_SPEC)
assert COLLECTOR_SPEC and COLLECTOR_SPEC.loader
sys.modules[COLLECTOR_SPEC.name] = COLLECTOR
COLLECTOR_SPEC.loader.exec_module(COLLECTOR)

CONSUMER_PATH = (
    Path(__file__).resolve().parents[2]
    / "batch_16_tushare_daily_replay_tools"
    / "tushare_daily_replay_consumer.py"
)
CONSUMER_SPEC = importlib.util.spec_from_file_location(
    "tushare_daily_replay_consumer_runtime", CONSUMER_PATH
)
CONSUMER = importlib.util.module_from_spec(CONSUMER_SPEC)
assert CONSUMER_SPEC and CONSUMER_SPEC.loader
sys.modules[CONSUMER_SPEC.name] = CONSUMER
CONSUMER_SPEC.loader.exec_module(CONSUMER)


def page_payload(fields: list[str], items: list[list[object]], has_more: bool = False) -> dict[str, object]:
    return {
        "code": 0,
        "message": "",
        "data": {
            "fields": fields,
            "items": items,
            "has_more": has_more,
            "count": len(items),
        },
        "request_id": "fake",
        "chart": None,
    }


class FakeTransport(COLLECTOR.TushareTransport):
    def __init__(self, scripted: dict[tuple[str, int], list[object]]) -> None:
        self.scripted = {key: list(values) for key, values in scripted.items()}
        self.calls: list[tuple[str, int, int, str]] = []

    def fetch_page(
        self,
        *,
        api_name: str,
        params: dict[str, object],
        fields: list[str],
        offset: int,
        limit: int,
        token: str,
        api_url: str,
    ) -> COLLECTOR.PageFetchResult:
        self.calls.append((api_name, offset, limit, api_url))
        key = (api_name, offset)
        if key not in self.scripted or not self.scripted[key]:
            raise AssertionError(f"Unexpected fake transport call: {key}")
        outcome = self.scripted[key].pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        if isinstance(outcome, COLLECTOR.PageFetchResult):
            return outcome
        return COLLECTOR.PageFetchResult(
            response_text=json.dumps(outcome, ensure_ascii=False, separators=(",", ":")),
            response_json=outcome,
            capture_time_utc=COLLECTOR.utc_now_iso(),
        )


class CollectorTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.snapshot_root = self.root / "snapshots"
        self.output_dir = self.root / "output"
        self.snapshot_root.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.token_env_var = "TUSHARE_TEST_TOKEN"
        os.environ.pop(self.token_env_var, None)

    def tearDown(self) -> None:
        os.environ.pop(self.token_env_var, None)
        self.temp_dir.cleanup()

    def _runtime_credential(self) -> str:
        return "".join(["unit", "_", "test", "_", "runtime", "_", "credential"])

    def _build_config(
        self,
        *,
        run_id: str = "run_001",
        reference_time_utc: str = "2026-09-01T12:30:00Z",
        max_retries: int = 2,
        page_limit: int = 2,
        snapshot_root: Path | None = None,
        output_dir: Path | None = None,
        api_url: str = COLLECTOR.OFFICIAL_API_URL,
    ) -> COLLECTOR.CollectorConfig:
        return COLLECTOR.CollectorConfig(
            snapshot_root=(snapshot_root or self.snapshot_root),
            output_dir=(output_dir or self.output_dir),
            token_env_var=self.token_env_var,
            run_id=run_id,
            timezone_name="Asia/Shanghai",
            post_close_cutoff_local="18:00",
            reference_time_utc=reference_time_utc,
            page_limit=page_limit,
            max_retries=max_retries,
            api_url=api_url,
        )

    def _assert_no_files_created(self) -> None:
        self.assertEqual(list(self.snapshot_root.rglob("*")), [])
        self.assertEqual(list(self.output_dir.rglob("*")), [])

    def _success_scripted(self, *, paginate_daily: bool = False) -> dict[tuple[str, int], list[object]]:
        trade_fields = ["exchange", "cal_date", "is_open", "pretrade_date"]
        stock_fields = ["ts_code", "symbol", "market", "exchange", "list_status", "list_date", "delist_date"]
        daily_fields = ["ts_code", "trade_date", "open", "high", "low", "close", "pre_close", "change", "pct_chg", "vol", "amount"]
        adj_fields = ["ts_code", "trade_date", "adj_factor"]

        scripted: dict[tuple[str, int], list[object]] = {
            ("trade_cal", 0): [
                page_payload(
                    trade_fields,
                    [
                        ["SSE", "20260902", 1, "20260901"],
                        ["SSE", "20260901", 1, "20260831"],
                        ["SSE", "20260831", 1, "20260828"],
                    ],
                ),
                page_payload(
                    trade_fields,
                    [
                        ["SZSE", "20260902", 1, "20260901"],
                        ["SZSE", "20260901", 1, "20260831"],
                        ["SZSE", "20260831", 1, "20260828"],
                    ],
                ),
            ],
            ("stock_basic", 0): [
                page_payload(
                    stock_fields,
                    [
                        ["600000.SH", "600000", "主板", "SSE", "L", "19991110", None],
                        ["000001.SZ", "000001", "主板", "SZSE", "L", "19910403", None],
                        ["430001.BJ", "430001", "北交所", "BSE", "L", "20200101", None],
                    ],
                )
            ],
            ("adj_factor", 0): [
                page_payload(
                    adj_fields,
                    [
                        ["600000.SH", "20260831", 1.0],
                        ["000001.SZ", "20260831", 2.0],
                        ["430001.BJ", "20260831", 3.0],
                    ],
                )
            ],
        }
        if paginate_daily:
            scripted[("daily", 0)] = [
                page_payload(
                    daily_fields,
                    [
                        ["600000.SH", "20260831", 10.0, 10.2, 9.9, 10.1, 10.0, 0.1, 1.0, 5000, 8000],
                        ["000001.SZ", "20260831", 12.0, 12.3, 11.8, 12.1, 12.0, 0.1, 0.8333, 3000, 4000],
                    ],
                    has_more=True,
                )
            ]
            scripted[("daily", 2)] = [
                page_payload(
                    daily_fields,
                    [
                        ["430001.BJ", "20260831", 8.0, 8.2, 7.9, 8.1, 8.0, 0.1, 1.25, 1000, 2000],
                    ],
                )
            ]
        else:
            scripted[("daily", 0)] = [
                page_payload(
                    daily_fields,
                    [
                        ["600000.SH", "20260831", 10.0, 10.2, 9.9, 10.1, 10.0, 0.1, 1.0, 5000, 8000],
                        ["000001.SZ", "20260831", 12.0, 12.3, 11.8, 12.1, 12.0, 0.1, 0.8333, 3000, 4000],
                        ["430001.BJ", "20260831", 8.0, 8.2, 7.9, 8.1, 8.0, 0.1, 1.25, 1000, 2000],
                    ],
                )
            ]
        return scripted

    def _run_success_collection(
        self, *, paginate_daily: bool = False, run_id: str = "run_001"
    ) -> tuple[dict[str, object], dict[str, Path]]:
        os.environ[self.token_env_var] = self._runtime_credential()
        config = self._build_config(run_id=run_id)
        transport = FakeTransport(self._success_scripted(paginate_daily=paginate_daily))
        result = COLLECTOR.collect_run(config, transport)
        paths = COLLECTOR.write_collection_outputs(result, config.output_dir)
        return result, paths

    def test_missing_token_generates_incomplete(self) -> None:
        result = COLLECTOR.collect_run(self._build_config(), FakeTransport({}))
        self.assertEqual(result["run_status"], COLLECTOR.INCOMPLETE_STATUS)
        self.assertEqual(result["collection_report"]["reason_counts"][COLLECTOR.TOKEN_MISSING_REASON], 1)

    def test_permission_error_generates_incomplete(self) -> None:
        os.environ[self.token_env_var] = self._runtime_credential()
        scripted = self._success_scripted()
        scripted[("stock_basic", 0)] = [COLLECTOR.PermissionDeniedError("permission denied")]
        result = COLLECTOR.collect_run(self._build_config(), FakeTransport(scripted))
        self.assertEqual(result["run_status"], COLLECTOR.INCOMPLETE_STATUS)
        self.assertEqual(result["collection_report"]["reason_counts"][COLLECTOR.PERMISSION_REASON], 1)

    def test_rate_limit_retries_then_succeeds(self) -> None:
        os.environ[self.token_env_var] = self._runtime_credential()
        scripted = self._success_scripted()
        scripted[("stock_basic", 0)] = [
            COLLECTOR.RateLimitError("limited"),
            COLLECTOR.RateLimitError("limited"),
            scripted[("stock_basic", 0)][0],
        ]
        result = COLLECTOR.collect_run(self._build_config(max_retries=2), FakeTransport(scripted))
        self.assertEqual(result["run_status"], COLLECTOR.SUCCESS_STATUS)
        self.assertEqual(result["collection_report"]["api_results"]["stock_basic_active"]["retry_count"], 2)

    def test_pagination_aggregates_rows(self) -> None:
        result, _ = self._run_success_collection(paginate_daily=True)
        self.assertEqual(result["run_status"], COLLECTOR.SUCCESS_STATUS)
        self.assertEqual(result["collection_report"]["api_results"]["daily_all_market"]["page_count"], 2)
        self.assertEqual(result["collection_report"]["api_results"]["daily_all_market"]["row_count"], 3)

    def test_empty_response_generates_incomplete(self) -> None:
        os.environ[self.token_env_var] = self._runtime_credential()
        scripted = self._success_scripted()
        daily_fields = ["ts_code", "trade_date", "open", "high", "low", "close", "pre_close", "change", "pct_chg", "vol", "amount"]
        scripted[("daily", 0)] = [page_payload(daily_fields, [])]
        result = COLLECTOR.collect_run(self._build_config(), FakeTransport(scripted))
        self.assertEqual(result["run_status"], COLLECTOR.INCOMPLETE_STATUS)
        self.assertEqual(result["collection_report"]["reason_counts"][COLLECTOR.EMPTY_RESPONSE_REASON], 1)

    def test_waiting_for_post_close_availability(self) -> None:
        os.environ[self.token_env_var] = self._runtime_credential()
        result = COLLECTOR.collect_run(
            self._build_config(reference_time_utc="2026-09-01T08:30:00Z"),
            FakeTransport(self._success_scripted()),
        )
        self.assertEqual(result["run_status"], COLLECTOR.WAITING_STATUS)
        self.assertEqual(result["collection_report"]["reason_counts"][COLLECTOR.WAITING_STATUS], 1)

    def test_duplicate_run_reuses_existing_snapshots_and_outputs(self) -> None:
        first_result, first_paths = self._run_success_collection(run_id="same_run")
        second_result, second_paths = self._run_success_collection(run_id="same_run")
        self.assertEqual(first_result["run_status"], COLLECTOR.SUCCESS_STATUS)
        self.assertEqual(second_result["run_status"], COLLECTOR.SUCCESS_STATUS)
        self.assertEqual(
            first_paths["manifest_path"].read_text(encoding="utf-8"),
            second_paths["manifest_path"].read_text(encoding="utf-8"),
        )
        self.assertEqual(
            first_paths["report_path"].read_text(encoding="utf-8"),
            second_paths["report_path"].read_text(encoding="utf-8"),
        )

    def test_same_run_different_content_fails(self) -> None:
        self._run_success_collection(run_id="same_run")
        os.environ[self.token_env_var] = self._runtime_credential()
        config = self._build_config(run_id="same_run", reference_time_utc="2026-09-02T12:30:00Z")
        with self.assertRaises(COLLECTOR.CollectorError):
            COLLECTOR.collect_run(config, FakeTransport(self._success_scripted()))

    def test_manifest_contains_complete_sha_fields(self) -> None:
        _, paths = self._run_success_collection()
        manifest = json.loads(paths["manifest_path"].read_text(encoding="utf-8"))
        self.assertEqual(manifest["run_status"], COLLECTOR.SUCCESS_STATUS)
        self.assertEqual(len(manifest["entries"]), 5)
        for entry in manifest["entries"]:
            self.assertEqual(entry["snapshot_role"], COLLECTOR.DERIVED_AGGREGATE_ROLE)
            snapshot_path = self.snapshot_root / entry["snapshot_path"]
            self.assertTrue(snapshot_path.exists())
            self.assertEqual(CONSUMER.sha256_file(snapshot_path), entry["snapshot_file_sha256"])

    def test_success_manifest_can_be_consumed_end_to_end(self) -> None:
        _, paths = self._run_success_collection()
        result = CONSUMER.consume_snapshots(paths["manifest_path"], self.snapshot_root)
        self.assertEqual(result.summary["status"], "SUCCESS")
        self.assertEqual(result.summary["normalized_output_row_count"], 2)

    def test_incomplete_manifest_is_rejected_by_consumer(self) -> None:
        result = COLLECTOR.collect_run(self._build_config(), FakeTransport({}))
        paths = COLLECTOR.write_collection_outputs(result, self.output_dir)
        with self.assertRaises(CONSUMER.ReplayValidationError):
            CONSUMER.consume_snapshots(paths["manifest_path"], self.snapshot_root)

    def test_token_never_appears_in_outputs(self) -> None:
        token_value = self._runtime_credential()
        os.environ[self.token_env_var] = token_value
        result = COLLECTOR.collect_run(self._build_config(), FakeTransport(self._success_scripted()))
        paths = COLLECTOR.write_collection_outputs(result, self.output_dir)
        texts = [
            paths["manifest_path"].read_text(encoding="utf-8"),
            paths["report_path"].read_text(encoding="utf-8"),
        ]
        for entry in result["manifest"]["entries"]:
            texts.append((self.snapshot_root / entry["snapshot_path"]).read_text(encoding="utf-8"))
            for page_info in result["collection_report"]["api_results"][entry["manifest_key"]]["page_response_chain"]:
                texts.append((self.snapshot_root / page_info["raw_page_path"]).read_text(encoding="utf-8"))
        self.assertTrue(all(token_value not in text for text in texts))

    def test_non_official_url_is_rejected_before_request(self) -> None:
        os.environ[self.token_env_var] = self._runtime_credential()
        config = self._build_config(api_url="https://evil.example.com")
        transport = FakeTransport({})
        with self.assertRaises(COLLECTOR.CollectorError):
            COLLECTOR.collect_run(config, transport)
        self.assertEqual(transport.calls, [])

    def test_redirect_is_rejected(self) -> None:
        os.environ[self.token_env_var] = self._runtime_credential()
        scripted = self._success_scripted()
        trade_fields = ["exchange", "cal_date", "is_open", "pretrade_date"]
        scripted[("trade_cal", 0)] = [
            COLLECTOR.RedirectBlockedError("Redirect blocked"),
            page_payload(
                trade_fields,
                [
                    ["SZSE", "20260902", 1, "20260901"],
                    ["SZSE", "20260901", 1, "20260831"],
                    ["SZSE", "20260831", 1, "20260828"],
                ],
            ),
        ]
        result = COLLECTOR.collect_run(self._build_config(), FakeTransport(scripted))
        self.assertEqual(result["run_status"], COLLECTOR.INCOMPLETE_STATUS)
        self.assertEqual(result["collection_report"]["reason_counts"][COLLECTOR.REDIRECT_REASON], 1)

    def test_repo_internal_snapshot_root_is_rejected(self) -> None:
        os.environ[self.token_env_var] = self._runtime_credential()
        internal_root = COLLECTOR.REPO_ROOT / "02_runtime" / "forbidden_snapshots"
        config = self._build_config(snapshot_root=internal_root)
        with self.assertRaises(COLLECTOR.CollectorError):
            COLLECTOR.collect_run(config, FakeTransport(self._success_scripted()))

    def test_repo_internal_output_dir_is_rejected(self) -> None:
        os.environ[self.token_env_var] = self._runtime_credential()
        internal_output = COLLECTOR.REPO_ROOT / "02_runtime" / "forbidden_output"
        config = self._build_config(output_dir=internal_output)
        with self.assertRaises(COLLECTOR.CollectorError):
            COLLECTOR.collect_run(config, FakeTransport(self._success_scripted()))

    def test_malicious_run_id_values_are_rejected_before_requests(self) -> None:
        os.environ[self.token_env_var] = self._runtime_credential()
        for bad_run_id in ("../bad", "..", ".", "a/b", "a\\b", "C:\\bad", "/abs"):
            with self.subTest(run_id=bad_run_id):
                transport = FakeTransport({})
                config = self._build_config(run_id=bad_run_id)
                with self.assertRaises(COLLECTOR.CollectorError):
                    COLLECTOR.collect_run(config, transport)
                self.assertEqual(transport.calls, [])
                self._assert_no_files_created()

    def test_multi_page_raw_hash_chain_and_capture_times_are_preserved(self) -> None:
        result, _ = self._run_success_collection(paginate_daily=True)
        daily_entry = next(
            entry for entry in result["manifest"]["entries"] if entry["manifest_key"] == "daily_all_market"
        )
        aggregate_snapshot = json.loads(
            (self.snapshot_root / daily_entry["snapshot_path"]).read_text(encoding="utf-8")
        )
        self.assertEqual(aggregate_snapshot["snapshot_role"], COLLECTOR.DERIVED_AGGREGATE_ROLE)
        self.assertEqual(aggregate_snapshot["source_response_origin"], COLLECTOR.DERIVED_AGGREGATE_ORIGIN)
        self.assertEqual(aggregate_snapshot["reference_time_utc"], "2026-09-01T12:30:00Z")
        self.assertNotEqual(aggregate_snapshot["capture_time_utc"], aggregate_snapshot["reference_time_utc"])
        self.assertEqual(len(aggregate_snapshot["derived_from_page_responses"]), 2)
        for page_info in aggregate_snapshot["derived_from_page_responses"]:
            raw_path = self.snapshot_root / page_info["raw_page_path"]
            raw_snapshot = json.loads(raw_path.read_text(encoding="utf-8"))
            self.assertEqual(raw_snapshot["snapshot_role"], COLLECTOR.RAW_PAGE_ROLE)
            self.assertEqual(raw_snapshot["source_response_sha256"], page_info["source_response_sha256"])
            self.assertEqual(CONSUMER.sha256_file(raw_path), page_info["snapshot_file_sha256"])
            self.assertEqual(raw_snapshot["capture_time_utc"], page_info["capture_time_utc"])
            self.assertNotEqual(raw_snapshot["capture_time_utc"], aggregate_snapshot["reference_time_utc"])


if __name__ == "__main__":
    unittest.main()
