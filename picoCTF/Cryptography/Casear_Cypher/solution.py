import string


def main():
    s = "cbdabldadbzlblzdzdzezczcczzczx"
    alphabet = string.ascii_lowercase

    for i in range(26):
        decoded = "".join(
            alphabet[(alphabet.index(c) - i) % 26]
            for c in s
        )
        print(i, decoded)


if __name__ == "__main__":
    main()

