import datetime as dt
import logging
import my_secrets
import os
import platform
import subprocess

from logging import Logger

logger: Logger = logging.getLogger(__name__)

now: dt = dt.date.today()
todays_date: str = now.strftime("%D").replace("/", "-")


def secure_copy(paths: list[str], month_name: str | None, year: str | None) -> set[str]:
    """
    Takes in a list of paths for location of website log files
    If historical
    param: paths
    param: month
    param: year
    """

    unzipped_paths: set = set()

    if year and month_name:
        month_name: str = month_name
        year: str = year

    else:
        month_name: str = now.strftime("%b")
        year: str = str(now.year)

    logger.info("STARTED: Remote download of site web logs")

    for path in paths:
        remote_zipped_filename: str = path + month_name + "-" + year + ".gz"

        local_unzipped_filename: str = remote_zipped_filename.split("/")[1]

        # COPY FROM REMOTE BLUEHOST SERVER DEPENDING ON PLATFORM
        if not platform.system() == "Windows":
            try:
                copy_command = os.system(
                    f"scp {my_secrets.user}@{my_secrets.bh_ip}:{remote_zipped_filename} {my_secrets.local_zipped_path}"
                )

                if copy_command == 0:
                    logger.info(
                        f"{path} {my_secrets.local_zipped_path} retrieved from bluehost server"
                    )
                    unzipped_paths.add(local_unzipped_filename)

                else:
                    logger.critical(f"Remote scp issue: {local_unzipped_filename}")

            except (OSError, FileNotFoundError) as err:
                logger.critical(f"see: {err} for more information")

        else:
            try:
                copy_command = f"pscp -batch {my_secrets.user}@{my_secrets.bh_ip}:{remote_zipped_filename} {my_secrets.local_zipped_path}"
                result = subprocess.check_output(copy_command)
                str_result: str = result.decode(encoding="utf-8")
                logger.info(str_result.strip())
                unzipped_paths.add(local_unzipped_filename)

            except subprocess.CalledProcessError as other_err:
                logger.error(other_err)

            except FileNotFoundError as file_e:
                logger.critical(f"File not found - {file_e}")

                continue

    logger.info("COMPLETED: Remote download of site web logs")

    return unzipped_paths
