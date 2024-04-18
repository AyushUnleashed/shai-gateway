from rich.logging import RichHandler
import logging

def get_logger(name: str):
    logging.basicConfig(
        level="INFO", format="%(message)s", datefmt="[%X]", handlers=[RichHandler()]
    )
    return logging.getLogger(name)
