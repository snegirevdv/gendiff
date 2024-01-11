from gendiff import logic


def main() -> None:
    args = logic.parse_arguments_from_command()
    return logic.generate_diff(args.first_file, args.second_file)


if __name__ == "__main__":
    main()
