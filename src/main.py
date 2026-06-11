from config import LOGS_PATH, REZERV_PATH


def main():
    if not REZERV_PATH.exists():
        REZERV_PATH.mkdir()

    if not LOGS_PATH.exists():
        LOGS_PATH.touch()

    from cli import cli

    cli()


if __name__ == "__main__":
    main()
