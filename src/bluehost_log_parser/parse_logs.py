import datetime as dt
import logging
import re

from bluehost_log_parser import my_secrets
from bluehost_log_parser.schema import LogEntry
from logging import Logger
from pathlib import Path
from typing import Any, Pattern, Match

logger: Logger = logging.getLogger(__name__)

now: dt.datetime = dt.datetime.now()
todays_date: str = now.strftime("%D").replace("/", "-")

# regex for Common Log Format (CLF)
weblog_with_response: Pattern[str] = re.compile(
    r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)" (.*?)\s'
)

# regex for unmatched above. Missing response size ("-")
weblog_without_response: Pattern[str] = re.compile(
    r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.*?)\] "(.*?)" (\d+) (-) "(.*?)" "(.*?)" (.*?)\s'
)

site_public_entries: list = []
site_soho_entries: list = []
site_sources: set = set()


def parse_matched(matched_response):
    user_agent_data: str | Any = matched_response.group(7)
    request = matched_response.group(3)

    try:
        user_agent: str | Any = user_agent_data.split(" ")[0].strip()
        client_os: str | Any = (
            user_agent_data.split(" ")[1].replace("(", "").replace(";", "")
        )
        client_version_split = user_agent_data.split(" ")[2:6]
        client_version = " ".join([c.replace(";", "") for c in client_version_split])
        client_version: str = "".join(
            [c.replace(")", "") for c in client_version_split]
        )

        client: str | Any = client_os + client_version

    except IndexError:
        user_agent = "NA"
        client = "NA"

    method, request, http_type = request.split()
    http_type: str | Any = http_type.replace("')", "")
    request: str | Any = request.replace("'[0]", "")

    entry: LogEntry = LogEntry(
        server_timestamp=matched_response.group(2),
        SOURCE=matched_response.group(1),
        METHOD=method,
        REQUEST=request,
        HTTP=http_type,
        REFERRER=matched_response.group(6),
        RESPONSE=matched_response.group(4),
        SIZE=matched_response.group(5),
        AGENT=user_agent,
        CLIENT=client,
        SITE=matched_response.group(8),
    )
    site_sources.add(entry.SOURCE)

    if entry.SOURCE == my_secrets.my_home_ip:
        site_soho_entries.append(entry)

    elif entry.SOURCE != my_secrets.my_home_ip:
        site_public_entries.append(entry)

    site_sources.add(entry.SOURCE)


def parse_unmatched(unmatched_response):
    user_agent_data = unmatched_response.group(7)
    request = unmatched_response.group(3)
    try:
        user_agent = user_agent_data.split(" ")[0].strip()
        client_os = user_agent_data.split(" ")[1].replace("(", "").replace(";", "")
        client_version_split: list[str] | Any = user_agent_data.split(" ")[2:6]
        client_version = " ".join([c.replace(";", "") for c in client_version_split])
        client_version = "".join([c.replace(")", "") for c in client_version_split])

        client = client_os + client_version

    except IndexError:
        user_agent = "NA"
        client = "NA"

    method, request, http_type = request.split()
    http_type = http_type.replace("')", "")
    request = request.replace("'[0]", "")

    entry: LogEntry = LogEntry(
        server_timestamp=unmatched_response.group(2),
        SOURCE=unmatched_response.group(1),
        METHOD=method,
        REQUEST=request,
        HTTP=http_type,
        REFERRER=unmatched_response.group(6),
        RESPONSE=unmatched_response.group(4),
        SIZE=unmatched_response.group(5),
        AGENT=user_agent,
        CLIENT=client,
        SITE=unmatched_response.group(8),
    )
    site_sources.add(entry.SOURCE)

    if entry.SOURCE == my_secrets.my_home_ip:
        site_soho_entries.append(entry)

    elif entry.SOURCE != my_secrets.my_home_ip:
        site_public_entries.append(entry)

    site_sources.add(entry.SOURCE)


def process_log(log_file: Path) -> tuple[set[str], list[LogEntry], list[LogEntry]]:
    """
    Function processes the log file for each web site.

    :param log_file: Path of logfile
    :return: tuple of unique ips and LogEntrys from PUBLIC and SOHO
    """
    matches = 0
    unmatched_responsees = 0
    unmatched = 0

    with open(f"{log_file}") as logs:
        for log in logs:
            matched_response: Match[str] | None = weblog_with_response.match(log)
            unmatched_response: Match[str] | None = weblog_without_response.match(log)
            if (
                matched_response
                and matched_response.group(1) != f"{my_secrets.my_bluehost_ip}"
            ):
                matches += 1
                parse_matched(matched_response)

            if (
                unmatched_response
                and unmatched_response.group(1) != f"{my_secrets.my_bluehost_ip}"
            ):
                unmatched_responsees += 1
                parse_unmatched(unmatched_response)

            else:
                if f"{my_secrets.my_bluehost_ip}" not in log:
                    logger.warning(f"still no re match: {log}")
                    unmatched += 1

    logger.info(
        f"\t\t{len(site_public_entries)} 'PUBLIC' logs with {len(set(site_sources))} unique source ip"
    )
    logger.info(f"\t\t{len(site_soho_entries)} 'SOHO' logs")
    logger.info(
        f"\t\t{len(site_public_entries) + len(site_soho_entries)} SITE LOG ENTRIES"
    )
    logger.info(f"\t\t{matches=} / {unmatched_responsees=} / {unmatched=}")

    return site_sources, site_public_entries, site_soho_entries


def start_processing(
    log_paths: list[Path], month_name_abbr: str | None, year_2_str: str | None
) -> tuple[list[str], list[LogEntry], list[LogEntry]]:
    """
    Function processes all current production website access logs.

    :param log_paths: list of Paths to unzipped logfiles
    :param month_name: abbreciated month name
    :param year: year as str
    :return: tuple of ip addresses, soho LogEntry, public LogEntry
    """

    all_public_log_entries: list = []
    all_soho_log_entries: list = []
    all_sources: list = []
    all_long_files = 0
    if year_2_str and month_name_abbr:
        month_name: str = month_name_abbr
        year: str = year_2_str

    else:
        month_name: str = now.strftime("%b")
        year: str = str(now.year)

    for p in log_paths:
        if month_name in p.name and year in p.name:
            logger.info(f"Parsing '{p.name}' logs")
            sources, public_logs, soho_logs = process_log(p)
            all_sources.extend(sources)
            all_public_log_entries.extend(public_logs)
            all_soho_log_entries.extend(soho_logs)

    if all_long_files > 0:
        logger.warning(
            f"\tLOG ENTRIES OVER 120 characers (all-sites) = {all_long_files}"
        )

    logger.info(
        f"PARSING COMPLETED: {len(all_public_log_entries) + len(all_soho_log_entries)} entries parsed."
    )

    return all_sources, all_public_log_entries, all_soho_log_entries
