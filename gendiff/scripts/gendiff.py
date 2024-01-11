import argparse


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compares two configuration files and shows a difference."
    )
    parser.add_argument("first_file")
    parser.add_argument("second_file")
    args: argparse.Namespace = parser.parse_args()
    print("Первый файл:", args.first_file)
    print("Второй файл:", args.second_file)


if __name__ == "__main__":
    main()
