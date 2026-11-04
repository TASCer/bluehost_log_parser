import datetime as dt
import gzip
import logging
import sys
from logging import Logger
from pathlib import Path

from bluehost_log_parser.utils.datetime_helper import get_monthname_short

logger: Logger = logging.getLogger(__name__)

now: dt.datetime = dt.datetime.now().astimezone()
unzipped_paths: set = set()


def refresh_unzipped_file(dir: Path, file: str):
    """
    Function removes current months log file(s) before proccessing. Alleviates numbered file name issues

    :param dir: _
    :param file: _description_
    """
    (dir / file).unlink()


def process(
    zipped_files: Path,
    unzipped_files: Path,
    month_name: str,
    year: str,
) -> list[Path]:
    """
    Function unzips file and saves to file

    param: paths
    arg: month
    arg: year
    returns: list of Paths
    """
    logger.info("<<< STARTED: UNZIPPING / SAVING DOWNLOADED WEBLOGS <<<")

    for root, _, files in unzipped_files.walk(top_down=False):
        current_year = now.year
        current_month = now.month
        current_month_abbr = get_monthname_short(
            arg_month=current_month, arg_year=current_year
        )
        for name in files:
            if current_month_abbr and str(current_year) in name:
                refresh_unzipped_file(root, file=name)

    local_files: list[Path] = []

    for zipped_file in zipped_files.iterdir():
        if zipped_file.name.startswith("cag"):
            local_file_name: str = zipped_file.with_suffix("").name.replace(
                "cag.bis.mybluehost.me", "tascs.net"
            )
        else:
            local_file_name: str = zipped_file.with_suffix("").name

        unzipped_file_path: Path = unzipped_files / local_file_name
        try:
            with (
                gzip.open(f"{zipped_file}", "rb") as zipped_file,
                open(
                    unzipped_file_path,
                    "wb",
                ) as unzipped_file,
            ):
                unzipped_file.write(zipped_file.read())
            local_files.append(unzipped_file_path)

        except FileNotFoundError as e:
            logger.critical(f"{e}")
            sys.exit()

    logger.info(">>> COMPLETED: UNZIPPING / SAVING DOWNLOADED WEBLOGS >>>")

    return local_files
