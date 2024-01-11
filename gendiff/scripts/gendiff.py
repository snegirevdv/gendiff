import argparse


def parse_arguments() -> argparse.Namespace():
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    return parser.parse_args()


def main() -> None:
    args: argparse.Namespace = parse_arguments()
    print("Первый файл:", args.first_file)
    print("Второй файл:", args.second_file)


if __name__ == "__main__":
    main()
