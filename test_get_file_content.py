from functions.get_file_content import get_file_content


def main():
    # Large file test (truncation)
    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")
    print()

    # Normal files
    print(get_file_content("calculator", "main.py"))
    print()
    print(get_file_content("calculator", "pkg/calculator.py"))
    print()

    # Error cases
    print(get_file_content("calculator", "/bin/cat"))
    print()
    print(get_file_content("calculator", "pkg/does_not_exist.py"))


if __name__ == "__main__":
    main()