from pathlib import Path
import runpy


if __name__ == "__main__":
    tool_path = Path(__file__).resolve().parent / "tools" / "generate_p0_subset.py"
    runpy.run_path(str(tool_path), run_name="__main__")
