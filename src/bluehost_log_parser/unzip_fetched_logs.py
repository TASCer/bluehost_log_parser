import datetime as dt
import gzip
import logging
import my_secrets

from datetime import datetime
from logging import Logger
from pathlib import Path

logger: Logger = logging.getLogger(__name__)

now: datetime = dt.datetime.now()

unzipped_paths: set = set()


def process(zipped_files: set[Path], unzipped_path: Path, month_name: str | None, year: str | None) -> set[str]:
    """
    Takes in a set of str paths for locally copied zipped bluehost website log files
    Unzips file and saves to file
    If historical args
    param: paths
    arg: month
    arg: year
    returns: set
    """
    logger.info("<<<<< STARTED: UNZIPPING AND SAVING DOWNLOADED WEBLOGS <<<<<")

    if year and month_name:
        month_name: str = month_name
        year: str = year

    else:
        month_name: str = now.strftime("%b")
        year: str = str(now.year)

    local_files: set = set()
    print("ZIP files path", zipped_files)
    print("UZIP PATH", unzipped_path)
    for zipped_file in zipped_files.iterdir():
        print("FILE:", zipped_file.name, type(zipped_file))
        try:
            local_file: str | None = zipped_file.name
            with gzip.open(f"{zipped_file}", "rb") as zipped_file:
                with open(
                    unzipped_path / local_file,
                    "wb",
                ) as unzipped_file:
                    unzipped_file.write(zipped_file.read())

        except (BaseException, FileNotFoundError) as e:
            logger.critical(f"{e}")
            local_file: None = None

        local_files.add(local_file)

    logger.info(">>>>> COMPLETED: UNZIPPING AND SAVING DOWNLOADED WEBLOGS >>>>>")

    return local_files
