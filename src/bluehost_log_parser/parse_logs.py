import datetime as dt
import logging
import re

from logging import Logger
from pathlib import Path
from typing import NamedTuple, Tuple
from bluehost_log_parser import my_secrets

logger: Logger = logging.getLogger(__name__)

now: dt.datetime = dt.datetime.now()
todays_date: str = now.strftime("%D").replace("/", "-")


class LogEntry(NamedTuple):
    server_timestamp: str
    SOURCE: str
    CLIENT: str
    AGENT: str
    ACTION: str
    FILE: str
    TYPE: str
    RES_CODE: str
    SIZE: int
    REF_URL: str
    REF_IP: str


def process(
    log_paths: set[Path], month_name: str | None, year: str | None
) -> Tuple[list[str], list[LogEntry], list[LogEntry]]:
    """
    Function takes a set of unzipped log paths and month and year
    Parses log file and returns tuple
    :param log_paths:
    :param month_name:
    :param year:
    :return:
    """
    all_log_entries: list = []
    all_my_log_entries: list = []
    all_sources: list = []
    all_long_files: list = []

    if year and month_name:
        month_name: str = month_name
        year: str = year

    else:
        month_name: str = now.strftime("%b")
        year: str = str(now.year)

    for p in log_paths:
        if month_name in p.name:
            logger.info(f"Parsing {p.name} logs")
            with open(f"{p}") as logs:
                site_log_entries: list = []
                site_sources: list = []
                site_long_files: list = []
                site_my_log_entries: list = []

                for log in logs:
                    basic_info: str = log.split('" "')[0]
                    ip: str = basic_info.split("- - ")[0]

                    if ":" in ip:
                        logger.warning(f"IPv6: {basic_info}")

                        continue

                    SOURCE: str = ip.rstrip()

                    # skip parsing system cron jobs performed on bluehost server
                    if SOURCE == f"{my_secrets.my_bluehost_ip}":
                        continue

                    basic_info: str = basic_info.split("- - ")[1]
                    server_timestamp: str = basic_info.split("]")[0][1:]

                    action_info: str = basic_info.split('"')[1]

                    try:
                        ACTION, FILE, TYPE = action_info.split(" ")

                    except (ValueError, IndexError) as e:
                        logger.error(f"\tACTION1 INFO SPLIT ERROR: {SOURCE}--{e}")
                        continue

                    if FILE.startswith("/:"):
                        FILE: str = FILE.replace(":", "")

                    if "'" in FILE:
                        FILE: str = FILE.replace("'", "")

                    if len(FILE) >= 120:
                        logger.warning(f"\tLONG FILENAME: {FILE}")
                        site_long_files.append(SOURCE)
                        all_long_files.append((server_timestamp, SOURCE))

                        try:
                            action_list: str = FILE.split("?")
                            action_file1: str = action_list[0]
                            action_file2: str = action_list[1][:80]

                        except IndexError:
                            try:
                                action_list: str = FILE.split("+")
                                action_file1: str = action_list[0]
                                action_file2: str = ""

                            except IndexError as e:
                                logger.error(e)

                        FILE = action_file1 + action_file2 + " *TRUNCATED*"

                    try:
                        result_info: str = basic_info.split('"')[2].strip()
                        RES_CODE, SIZE = result_info.split(" ")

                    except ValueError as e:
                        logger.error(f"Possible bot, check logs -> {e}")
                        continue

                    agent_info: str = log.split('" "')[1]
                    agent_list: list = agent_info.split(" ")
                    AGENT: str = agent_list[0].replace('"', "")

                    if AGENT.startswith("-"):
                        AGENT: str = "NA"

                    if AGENT.startswith("'b'"):
                        CLIENT: str = AGENT.replace("'b'", "")

                    elif AGENT.startswith("'"):
                        AGENT: str = AGENT.replace("'", "")

                    REF_IP: str = agent_list[-1].strip()
                    REF_URL: str = agent_list[-2]

                    # FINDS ALL BETWEEN (    )
                    client: list[str] = re.findall(r"\((.*?)\)", log)

                    if not client:
                        CLIENT, client_format = 2 * ("NA",)

                    elif len(client) == 1:
                        client_os: str = client[0]
                        CLIENT: str = client_os.replace(";", "").lstrip()

                    else:
                        client_os: str = client[0]
                        CLIENT: str = client_os.replace(";", "").lstrip()

                    if "'" in CLIENT:
                        CLIENT: str = CLIENT.replace("'", "")

                    site_sources.append(SOURCE)
                    all_sources.append(SOURCE)
                    entry: LogEntry = LogEntry(
                        server_timestamp=server_timestamp,
                        SOURCE=SOURCE,
                        ACTION=ACTION,
                        FILE=FILE,
                        TYPE=TYPE,
                        REF_URL=REF_URL,
                        REF_IP=REF_IP,
                        RES_CODE=RES_CODE,
                        SIZE=SIZE,
                        AGENT=AGENT,
                        CLIENT=CLIENT,
                    )

                    if SOURCE == my_secrets.my_home_ip:
                        all_my_log_entries.append(entry)
                        site_my_log_entries.append(entry)

                    elif SOURCE != my_secrets.my_home_ip:
                        site_log_entries.append(entry)
                        all_log_entries.append(entry)

                logger.info(
                    f"\t\t{len(site_log_entries)} NON SOHO logs with {len(set(site_sources))} unique source ip"
                )
                logger.info(f"\t\t{len(site_my_log_entries)} SOHO logs")
                logger.info(
                    f"\t\t{len(site_log_entries) + len(site_my_log_entries)} SITE LOG ENTRIES"
                )

                if len(site_long_files) >= 1:
                    logger.warning(
                        f"\t\t{len(site_long_files)} long file names encountered."
                    )
        else:
            continue

    if len(all_long_files) > 0:
        logger.warning(
            f"\tLOG ENTRIES OVER 120 characers (all-sites) = {len(all_long_files)}"
        )

    logger.info("COMPLETED WEBLOG PARSING")

    return all_sources, all_log_entries, all_my_log_entries


if __name__ == "__main__":
    pass
    # process()
