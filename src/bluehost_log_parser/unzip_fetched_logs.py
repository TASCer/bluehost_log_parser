import datetime as dt
import gzip
import logging

from datetime import datetime
from logging import Logger
from pathlib import Path

logger: Logger = logging.getLogger(__name__)

now: datetime = dt.datetime.now()

unzipped_paths: set = set()


def process(
    zipped_files: Path,
    unzipped_path: Path,
    month_name: str,
    year: str,
) -> list[Path]:
    """
    Takes in a set of str paths for locally copied zipped bluehost website log files
    Unzips file and saves to file
    If historical args
    param: paths
    arg: month
    arg: year
    returns: set
    """
    logger.info("<<<<< STARTED: UNZIPPING / SAVING DOWNLOADED WEBLOGS <<<<<")

    for root, _, files in unzipped_path.walk(top_down=False):
        for name in files:
            (root / name).unlink()

    local_files: list = []

    for zipped_file in zipped_files.iterdir():
        try:
            local_file_name: str | None = zipped_file.with_suffix("").name
            unzipped_file_path = unzipped_path / local_file_name
            with gzip.open(f"{zipped_file}", "rb") as zipped_file:
                with open(
                    unzipped_file_path,
                    "wb",
                ) as unzipped_file:
                    unzipped_file.write(zipped_file.read())

        except (BaseException, FileNotFoundError) as e:
            logger.critical(f"{e}")
            local_file_name: None = None

        local_files.append(unzipped_file_path)

    logger.info(">>>>> COMPLETED: UNZIPPING / SAVING DOWNLOADED WEBLOGS >>>>>")

    return local_files
