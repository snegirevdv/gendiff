#!/usr/bin/env python3

import argparse
import gendiff


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument(
        "-f", "--format",
        metavar="FORMAT",
        choices=["plain", "json"],
        help="set format of output",
        default="plain",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()
    return gendiff.generate_diff(args.first_file, args.second_file)


if __name__ == "__main__":
    main()
