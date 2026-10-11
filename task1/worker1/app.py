import argparse
import shutil
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Select the largest input file by size in bytes."
    )
    parser.add_argument("--input-dir", type=Path, default=Path("/var/data"))
    parser.add_argument("--output-dir", type=Path, default=Path("/var/result"))
    args = parser.parse_args()

    try:
        if not args.input_dir.is_dir():
            raise ValueError(f"Input directory not found: {args.input_dir}")

        files = [
            path for path in args.input_dir.iterdir()
            if path.is_file() and path.name != ".gitkeep"
        ]
        if not files:
            raise ValueError("Input directory contains no data files.")

        selected = sorted(
            files,
            key=lambda path: (-path.stat().st_size, path.name),
        )[0]

        args.output_dir.mkdir(parents=True, exist_ok=True)
        destination = args.output_dir / "data.txt"
        shutil.copyfile(selected, destination)

        print(f"Selected file: {selected.name}")
        print(f"Size: {selected.stat().st_size} bytes")
        print(f"Copied to: {destination}")
        return 0

    except (OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
