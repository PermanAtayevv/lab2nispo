import argparse
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Multiply the first and last integers in data.txt."
    )
    parser.add_argument("--input-dir", type=Path, default=Path("/var/data"))
    parser.add_argument("--output-dir", type=Path, default=Path("/var/result"))
    args = parser.parse_args()

    try:
        source = args.input_dir / "data.txt"
        tokens = source.read_text(encoding="utf-8-sig").split()

        if not tokens:
            raise ValueError("Input file contains no integers.")

        numbers = []
        for position, token in enumerate(tokens, start=1):
            try:
                numbers.append(int(token))
            except ValueError:
                raise ValueError(
                    f"Invalid integer at position {position}: {token!r}"
                ) from None

        result = numbers[0] * numbers[-1]

        args.output_dir.mkdir(parents=True, exist_ok=True)
        destination = args.output_dir / "result.txt"
        destination.write_text(f"{result}\n", encoding="utf-8")

        print(f"First integer: {numbers[0]}")
        print(f"Last integer: {numbers[-1]}")
        print(f"Result: {result}")
        print(f"Saved to: {destination}")
        return 0

    except (OSError, UnicodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
