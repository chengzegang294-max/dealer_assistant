from __future__ import annotations

import argparse
from collections import deque
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--tail-lines", type=int, required=True)
    args = parser.parse_args()

    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    tail_lines = int(args.tail_lines)
    if tail_lines <= 0:
        raise ValueError("--tail-lines must be > 0")

    with input_path.open("r", encoding="utf-8", errors="replace") as f:
        header = f.readline()
        if not header:
            raise ValueError("empty input file")
        buf: deque[str] = deque(maxlen=tail_lines)
        for line in f:
            buf.append(line)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        f.write(header)
        for line in buf:
            f.write(line)

    print("input={0}".format(input_path))
    print("output={0}".format(output_path))
    print("tail_lines={0}".format(tail_lines))
    print("written_lines={0}".format(len(buf) + 1))


if __name__ == "__main__":
    main()

