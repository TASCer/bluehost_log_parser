import logging
import os
import platform
import subprocess
import sys
from logging import Logger
from pathlib import Path

from dotenv import load_dotenv

from bluehost_log_parser.utils import mailer, ssh_agent_check

logger: Logger = logging.getLogger(__name__)

load_dotenv()


def secure_copy(
    remote_log_paths: list[str],
    local_zipped_path: Path,
    month_name: str,
    year: str,
) -> bool:
    """
    Function copies webserver host log files locally.

    :param remote_log_paths: list of Paths
    :param local_zipped_path: location to unzip log file
    :param month_name: short month name
    :param year: year as str

    :return: True if all log files copied locally
    """
    logger.info("STARTED secure download of remote website logfiles:")

    if not ssh_agent_check.is_ssh_agent_running_env():
        return False

    for path in remote_log_paths:
        remote_zipped_filename: str = path + month_name + "-" + year + ".gz"
        source = f"{os.environ['BLUEHOST_USER']}@{os.environ['BLUEHOST_SERVER_IP']}:{remote_zipped_filename}"
        destination = f"{local_zipped_path}"

        if platform.system() != "Windows":
            command = ["scp", source, destination]

            try:
                result = subprocess.run(command, check=True, capture_output=True)

                if result:
                    logger.info(f"\t'{remote_zipped_filename.split('/')[2]}' copied")
                else:
                    logger.critical(
                        "scp issue: BAD CREDS or ssh-agent not running/loaded with key"
                    )
                    mailer.send_mail(
                        "SCP FAILED",
                        "BAD CREDS or ssh-agent not running/loaded with key",
                    )
                    sys.exit()

            except (OSError, FileNotFoundError) as err:
                logger.critical(f"see: {err} for more information")
                mailer.send_mail(
                    subject="**WEBLOG SCP FAILURE",
                    text="check ssh agent process and key",
                )

            logger.info("COMPLETED secure download of remote website logfiles:")

        # NEEDS TESTING
        if platform.system() != "Linux":
            command = ["pscp", source, destination]

            try:
                result = subprocess.run(command, check=True, capture_output=True)

                if result:
                    logger.info(f"\t'{remote_zipped_filename.split('/')[2]}' copied")
                else:
                    logger.critical(
                        "scp issue: BAD CREDS or ssh-agent not running/loaded with key"
                    )
                    mailer.send_mail(
                        "SCP FAILED",
                        "BAD CREDS or ssh-agent not running/loaded with key",
                    )
                    sys.exit()

            except (OSError, FileNotFoundError) as err:
                logger.critical(f"see: {err} for more information")
                mailer.send_mail(
                    subject="**WEBLOG SCP FAILURE",
                    text="check ssh agent process and key",
                )

            logger.info("COMPLETED secure download of remote website logfiles:")

    return True
