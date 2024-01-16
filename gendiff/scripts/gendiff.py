#!/usr/bin/env python3

import argparse

import gendiff
from gendiff.format import json_format, plain, stylish


def parse_arguments_from_command() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    parser.add_argument(
        "-f", "--format",
        metavar="FORMAT",
        choices=["plain", "json", "stylish"],
        help="set format of output",
        default="stylish",
    )
    return parser.parse_args()


def parse_formatter(report_format):
    match report_format:
        case "plain": return plain.plain
        case "json": return json_format.json_format
    return stylish.stylish


def main() -> None:
    args = parse_arguments_from_command()
    formatter = parse_formatter(args.format)
    return gendiff.generate_diff(args.first_file, args.second_file, formatter)
