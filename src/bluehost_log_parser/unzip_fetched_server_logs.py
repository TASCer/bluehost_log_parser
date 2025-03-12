import datetime as dt
import gzip
import logging
import my_secrets

from datetime import datetime
from logging import Logger

logger: Logger = logging.getLogger(__name__)

now: datetime = dt.datetime.now()


def process(files: set[str], month_name: str | None, year: str | None) -> set[str]:
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

    for file in files:
        try:
            local_file: str | None = file.split(".")[0]
            with gzip.open(f"{my_secrets.local_zipped_path}{file}", "rb") as zipped_file:
                with open(
                    f"{my_secrets.local_unzipped_path}{local_file}_{month_name}-{year}",
                    "wb",
                ) as unzipped_file:
                    unzipped_file.write(zipped_file.read())

        except (BaseException, FileNotFoundError) as e:
            logger.critical(f"{e}")
            local_file: None = None

        local_files.add(local_file)

    logger.info(">>>>> COMPLETED: UNZIPPING AND SAVING DOWNLOADED WEBLOGS >>>>>")

    return local_files
