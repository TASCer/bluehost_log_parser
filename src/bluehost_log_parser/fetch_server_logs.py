import datetime as dt
import logging
import os
import platform
import subprocess

from bluehost_log_parser.utils import ssh_agent_check
from bluehost_log_parser import my_secrets, mailer
from datetime import date
from logging import Logger
from pathlib import Path

logger: Logger = logging.getLogger(__name__)

now: date = dt.date.today()


# TODO remove old files or specify via date. Check if June & July get parsed
def secure_copy(
    remote_log_paths: list[str],
    local_zipped_path: Path,
    month_name: str | None,
    year: str | None,
) -> bool:
    """
    Takes in a list of paths for location of website log files
    If historical
    param: paths
    param: month
    param: year
    """
    if not ssh_agent_check.is_ssh_agent_running_env():
        return False

    if year and month_name:
        month_name: str = month_name
        year: str = year

    else:
        month_name: str = now.strftime("%b")
        year: str = str(now.year)

    logger.info("STARTED: secure download of remote website logfiles")

    for path in remote_log_paths:
        remote_zipped_filename: str = path + month_name + "-" + year + ".gz"

        if not platform.system() == "Windows":
            try:
                copy_command: int = os.system(
                    f"scp {my_secrets.bluehost_user}@{my_secrets.my_bluehost_ip}:{remote_zipped_filename} {local_zipped_path}"
                )

                if copy_command == 0:
                    logger.info(f"\t{remote_zipped_filename.split('/')[1]}")
                else:
                    logger.critical(
                        "scp issue: BAD CREDS or ssh-agent not running/loaded with key"
                    )
                    exit()

            except (OSError, FileNotFoundError) as err:
                logger.critical(f"see: {err} for more information")
                mailer.send_mail(
                    subject="**WEBLOG SCP FAILURE",
                    text="check ssh agent process and key",
                )
                exit()

        else:
            try:
                copy_command = f"pscp -batch {my_secrets.user}@{my_secrets.my_bluehost_ip}:{remote_zipped_filename} {local_zipped_path}"
                response = subprocess.check_output(executable=copy_command)
                result: str = response.decode(encoding="utf-8")
                logger.info(result.strip())

            except subprocess.CalledProcessError as other_err:
                logger.error(other_err)

            except FileNotFoundError as file_e:
                logger.critical(f"File not found - {file_e}")

                continue

    return True

    logger.info("COMPLETED: download of remote website logs")
