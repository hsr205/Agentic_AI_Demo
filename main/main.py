from logging import Logger

from logger.logger import AppLogger


def main() -> int:
    logger: Logger = AppLogger().get_logger(__name__)
    try:
        logger.info(f"Hello from main() method")
        return 0

    except Exception as e:
        logger.exception(f"Exception Thrown: {e}")
        raise Exception(e)


if __name__ == "__main__":
    main()
