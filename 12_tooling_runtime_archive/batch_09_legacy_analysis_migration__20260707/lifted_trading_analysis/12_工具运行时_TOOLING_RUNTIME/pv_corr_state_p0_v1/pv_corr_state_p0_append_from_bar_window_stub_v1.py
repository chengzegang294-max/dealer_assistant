from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


RUNTIME_DIR = Path(__file__).resolve().parent
PARAMS_PATH = RUNTIME_DIR / "pv_corr_state_p0_runtime_params_template_v1.json"


def load_params() -> dict:
    with PARAMS_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def ensure_archive_only_run_allowed() -> None:
    if os.environ.get("ALLOW_ARCHIVE_ONLY_RUN") != "1":
        raise SystemExit(
            "ARCHIVE_ONLY: set ALLOW_ARCHIVE_ONLY_RUN=1 and use repo-first entry points under "
            "01_active_objects/ 02_runtime/ 04_active_main_docs/ before running this legacy stub."
        )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="print interface binding status only",
    )
    args = parser.parse_args()
    ensure_archive_only_run_allowed()

    params = load_params()
    interface = params["bar_window_interface"]
    boundary = params["execution_boundary"]
    target_csv = Path(params["runtime_dir"]) / interface["append_target"]

    print("interface_mode={0}".format("dry_run"))
    print("binding_state={0}".format(interface["binding_state"]))
    print("source_kind={0}".format(interface["source_kind"]))
    print("allow_live_binding={0}".format(boundary["allow_live_binding"]))
    print("allow_bar_window_append={0}".format(boundary["allow_bar_window_append"]))
    print("target_csv_exists={0}".format(target_csv.exists()))
    print("append_target={0}".format(target_csv))
    print(
        "required_fields={0}".format(
            json.dumps(
                [
                    interface["window_bars_field"],
                    interface["corr_field"],
                    interface["price_change_field"],
                    interface["volume_change_field"],
                ],
                ensure_ascii=True,
            )
        )
    )
    print("write_attempted=false")
    print("dry_run_only=true")


if __name__ == "__main__":
    main()
