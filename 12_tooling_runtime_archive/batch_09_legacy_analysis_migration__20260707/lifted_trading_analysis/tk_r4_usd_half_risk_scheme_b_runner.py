from pathlib import Path
import os
import runpy


if __name__ == "__main__":
    if not os.environ.get("ALLOW_ARCHIVE_ONLY_RUN"):
        raise RuntimeError(
            "ARCHIVE_ONLY: legacy runner. Set ALLOW_ARCHIVE_ONLY_RUN=1 to run intentionally."
        )
    tool_path = Path(__file__).resolve().parent / "tools" / "tk_r4_usd_half_risk_scheme_b_runner.py"
    runpy.run_path(str(tool_path), run_name="__main__")
