#!/usr/bin/env python3

import argparse

import gendiff
from gendiff.constants import JSON, PLAIN, STYLISH


def parse_arguments_from_command() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument(
        "-f",
        "--format",
        metavar="FORMAT",
        choices=[PLAIN, JSON, STYLISH],
        help="set format of output",
        default=STYLISH,
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments_from_command()
    print(gendiff.generate_diff(args.first_file, args.second_file, args.format))
