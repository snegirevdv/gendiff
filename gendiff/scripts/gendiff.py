import gendiff


def main() -> None:
    args = gendiff.parse_arguments_from_command()
    return gendiff.generate_diff(args.first_file, args.second_file)


if __name__ == "__main__":
    main()
