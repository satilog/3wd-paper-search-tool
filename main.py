import argparse


def main():
    parser = argparse.ArgumentParser(description="Paper Search Tool")
    parser.add_argument(
        "--config",
        type=str,
        default="./config/config.yaml",
        help="Path to the config file",
    )
    args = parser.parse_args()

    print(args)


if __name__ == "__main__":
    main()
