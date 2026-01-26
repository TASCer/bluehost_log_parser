import datetime as dt
import gzip
import logging

from datetime import datetime
from logging import Logger
from pathlib import Path
from bluehost_log_parser.utils.datetime_helper import get_monthname_short

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
    logger.info("<<< STARTED: UNZIPPING / SAVING DOWNLOADED WEBLOGS <<<")

    for root, _, files in unzipped_path.walk(top_down=False):
        current_year = now.year
        current_month = now.month
        current_month_abbr = get_monthname_short(
            arg_month=current_month, arg_year=current_year
        )
        for name in files:
            if current_month_abbr and str(current_year) in name:
                (root / name).unlink()

    local_files: list[Path] = []

    for zipped_file in zipped_files.iterdir():
        if zipped_file.name.startswith("cag"):
            local_file_name: str = zipped_file.with_suffix("").name.replace(
                "cag.bis.mybluehost.me", "tascs.net"
            )
        else:
            local_file_name: str = zipped_file.with_suffix("").name

        unzipped_file_path: Path = unzipped_path / local_file_name
        try:
            with gzip.open(f"{zipped_file}", "rb") as zipped_file:
                with open(
                    unzipped_file_path,
                    "wb",
                ) as unzipped_file:
                    unzipped_file.write(zipped_file.read())
            local_files.append(unzipped_file_path)

        except (BaseException, FileNotFoundError) as e:
            logger.critical(f"{e}")

    logger.info(">>> COMPLETED: UNZIPPING / SAVING DOWNLOADED WEBLOGS >>>")

    return local_files
