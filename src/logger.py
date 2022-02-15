import logging
import coloredlogs
from sys import stdout

from src.model import Board, Thread, Post
from src.utils import FileManager


class Logger:

    def __init__(self):
        coloredlogs.install()

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.StreamHandler(stdout)
            ]
        )

    def successfully_got_resource(self, r: object) -> None:
        match r:
            case Board():
                logging.info(f"Retrieved threads catalog from board '/{r.id}'")
            case Thread():
                logging.info(
                    f"Retrieved posts catalog from board '/{r.board.id}', thread '{r.id}'")
            case Post():
                logging.info(
                    f"Downloaded file {r.file.filename}{r.file.ext}({FileManager.get_file_size(r.file.fsize)}) from board '/{r.thread.board.id}', thread '{r.thread.id}' as {r.file.id}{r.file.ext}")
            case _:  # Should not happen at all
                logging.exception("Retrieved unknown resource")

    def failed_to_get_resource(self, r: object) -> None:
        match r:
            case Board():
                logging.exception(
                    f"Failed to retrieve threads catalog from board '/{r.id}'")
            case Thread():
                logging.exception(
                    f"Failed to retrieve posts catalog from board '/{r.board.id}', thread '{r.id}'")
            case Post():
                logging.exception(
                    f"Failed to download file {r.file.id}.{r.file.ext}({FileManager.get_file_size(r.file.fsize)}) board '/{r.thread.board.id}', thread '{r.thread.id}'")
            case _:  # Should not happen at all
                logging.exception("Failed to get unknown resource")

    def requested_resource_not_modified(self, r: object) -> None:
        match r:
            case Board():
                logging.info(
                    f"Board '/{r.id}' was not modified since last request")
            case Thread():  # Should not happen at all
                logging.info(
                    f"Posts catalog from board '/{r.board.id}', thread '{r.id}' was not modified since last request")
            case Post():  # Should not happen at all
                logging.info(
                    f"Downloaded File {r.file.filename}.{r.file.ext} board '/{r.thread.board.id}', thread '{r.thread.id}' was not modified since last request")
            case _:  # Should not happen at all
                logging.exception(
                    "Unknown resource was not modified since last request")
