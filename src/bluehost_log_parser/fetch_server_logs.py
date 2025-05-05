import datetime as dt
import logging
import os
import platform
import subprocess

from bluehost_log_parser import my_secrets, mailer
from logging import Logger
from pathlib import Path

logger: Logger = logging.getLogger(__name__)

now: dt = dt.date.today()


def secure_copy(
    remote_log_paths: list[str],
    local_zipped_path: Path,
    month_name: str | None,
    year: str | None,
) -> None:
    """
    Takes in a list of paths for location of website log files
    If historical
    param: paths
    param: month
    param: year
    """

    if year and month_name:
        month_name: str = month_name
        year: str = year

    else:
        month_name: str = now.strftime("%b")
        year: str = str(now.year)

    logger.info("STARTED: downloading of remote website logs")

    for path in remote_log_paths:
        remote_zipped_filename: str = path + month_name + "-" + year + ".gz"

        if not platform.system() == "Windows":
            try:
                copy_command = os.system(
                    f"scp {my_secrets.bluehost_user}@{my_secrets.my_bluehost_ip}:{remote_zipped_filename} {local_zipped_path}"
                )

                if copy_command == 0:
                    logger.info(
                        f"\t{remote_zipped_filename.split('/')[1]} securely copied"
                    )
                else:
                    logger.critical(f"Remote scp issue: {remote_zipped_filename}")
                    exit()

            except (OSError, FileNotFoundError) as err:
                logger.critical(f"see: {err} for more information")
                # SEND EMAIL?
                # mailer.send_mail(subject="**WEBLOG SCP FAILURE", text="check ssh agent process and key")
                exit()

        else:
            try:
                copy_command = f"pscp -batch {my_secrets.user}@{my_secrets.bh_ip}:{remote_zipped_filename} {my_secrets.local_zipped_path}"
                result = subprocess.check_output(copy_command)
                str_result: str = result.decode(encoding="utf-8")
                logger.info(str_result.strip())

            except subprocess.CalledProcessError as other_err:
                logger.error(other_err)

            except FileNotFoundError as file_e:
                logger.critical(f"File not found - {file_e}")

                continue

    logger.info("COMPLETED: download of remote website logs")
