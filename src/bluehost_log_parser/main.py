import argparse
import logging

from bluehost_log_parser import db_checks
from bluehost_log_parser import fetch_whois_data

from bluehost_log_parser import fetch_server_logs
from bluehost_log_parser import insert_activity
from bluehost_log_parser import insert_unique_sources
from bluehost_log_parser.utils import mailer, datetime_helper
from bluehost_log_parser import parse_logs
from bluehost_log_parser import unzip_fetched_logs
from bluehost_log_parser import update_sources
from logging import Logger, Formatter
from pathlib import Path

PROJECT_ROOT: Path = Path.cwd()
LOGGER_ROOT: Path = Path.cwd().parent.parent

root_logger: Logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

fh = logging.FileHandler(f"{LOGGER_ROOT}/{datetime_helper.get_logger_date()}.log")
fh.setLevel(logging.DEBUG)

formatter: Formatter = logging.Formatter(
    "%(asctime)s - %(filename)s -%(lineno)d - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)

root_logger.addHandler(fh)

logger: Logger = logging.getLogger(__name__)

# NOTE: REMOTE BLUEHOST SERVER'S BASE LOG PATHS. **DOES NOT INCLUDE** "month-year.gz"
REMOTE_TASCS_BASE_PATH: str = "logs/cag.bis.mybluehost.me-ssl_log-"
REMOTE_HOA_BASE_PATH: str = "logs/hoa.tascs.net-ssl_log-"
REMOTE_ROADSPIES_BASE_PATH: str = "logs/roadspies.cag.bis.mybluehost.me-ssl_log-"

LOCAL_ZIPPED_PATH: Path = PROJECT_ROOT / "input" / "zipped_logfiles"
Path(LOCAL_ZIPPED_PATH).mkdir(parents=True, exist_ok=True)
LOCAL_UNZIPPED_PATH: Path = PROJECT_ROOT / "output" / "unzipped_logfiles"
Path(LOCAL_UNZIPPED_PATH).mkdir(parents=True, exist_ok=True)

REMOTE_LOGFILE_BASE_PATHS: list = [
    REMOTE_TASCS_BASE_PATH,
    REMOTE_HOA_BASE_PATH,
]


def database_check() -> bool:
    """
    Function checks if database schema and tables are available.

    :return: True if available
    """
    logger.info("CHECKING RDBMS AVAILABILITY")
    have_database: bool = db_checks.schema()
    have_tables: bool = db_checks.tables()

    if have_database and have_tables:
        logger.info("\t\t+ONLINE+")
        return True

    else:
        logger.error(f"-OFFLINE- {have_database} / TABLES: {have_tables}**")
        return False


def main(month: int | None, year: int | None) -> None:
    """
    Function controls the application.

    :param month: optional month number to process another month's log
    :param year: optional year number to process another month's log
    """
    logger.info("*** STARTING BLUEHOST LOG PARSER ***")

    if month and year:
        month_name_abbr: str = datetime_helper.get_monthname_short(
            arg_year=year, arg_month=month
        )
        year_2_str: str = str(year)

    else:
        month_name_abbr: str = datetime_helper.get_now().strftime("%b")
        year_2_str: str = str(datetime_helper.get_now().year)

    logs_fetched: bool = fetch_server_logs.secure_copy(
        REMOTE_LOGFILE_BASE_PATHS, LOCAL_ZIPPED_PATH, month_name_abbr, year_2_str
    )

    if logs_fetched:
        unzipped_log_files: list[Path] = unzip_fetched_logs.process(
            LOCAL_ZIPPED_PATH, LOCAL_UNZIPPED_PATH, month_name_abbr, year_2_str
        )

        source_ips, public_processed_logs, my_processed_logs = (
            parse_logs.start_processing(unzipped_log_files, month_name_abbr, year_2_str)
        )

        unique_sources: set = set(source_ips)
        no_country_name: list[str] = insert_unique_sources.inserts(unique_sources)
        if no_country_name:
            results: list[str] = fetch_whois_data.get_country(no_country_name)
            update_sources.whois_updates(results)

        else:
            logger.info("Whois Information Not Needed.")

        insert_activity.update_log_tables(public_processed_logs, my_processed_logs)

        logger.info("***** COMPLETED WEB LOG PROCESSING *****")
        # mailer.send_mail(
        #     subject="COMPLETED", text="Processing completed without incident"
        # )

    else:
        mailer.send_mail(
            subject="ERROR: During Processing",
            text="Error downloading from Bluehost, check log",
            attachment_path=Path.cwd().parent.parent
            / f"{datetime_helper.get_logger_date()}.log",
        )


if __name__ == "__main__":
    if database_check():
        parser = argparse.ArgumentParser(description="ADHOC month/year log processing")
        parser.add_argument(
            "-m",
            "--month",
            type=int,
            choices=[m for m in range(1, 13)],
            help="Enter a Month number: 1-12",
        )
        parser.add_argument(
            "-y",
            "--year",
            type=int,
            choices=[y for y in range(2019, datetime_helper.get_now().year + 1)],
            help="Enter full year i.e: 2022",
        )
        args = parser.parse_args()

        if all(vars(args).values()):
            main(**vars(args))

        elif any(vars(args).values()):
            print(f"Need both -m month AND -y year. Args passed: {vars(args)}")
            logger.error(f"Need both -m month AND -y year. Args passed: {vars(args)}")

        main(**vars(args))

    else:
        print(
            f"Database has an issue. Check log: '{datetime_helper.get_logger_date()}.log' in project root"
        )
        logger.error("Database has an issue")
