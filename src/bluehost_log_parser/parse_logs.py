# TODO What to do with unmatched logs? Seems missing size value causing issues. Rematching on fail works. Need to refactor as redundant
import datetime as dt
import logging
import re

from logging import Logger
from pathlib import Path
from bluehost_log_parser import my_secrets
from bluehost_log_parser.schema import LogEntry

logger: Logger = logging.getLogger(__name__)

now: dt.datetime = dt.datetime.now()
todays_date: str = now.strftime("%D").replace("/", "-")

# regex for Common Log Format (CLF)
weblog_pattern = re.compile(
    r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.*?)\] "(.*?)" (\d+) (\d+) "(.*?)" "(.*?)" (.*?)\s'
)

# regex for unmatched. Missing file size digits.
weblog_pattern_no_match = re.compile(
    r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.*?)\] "(.*?)" (\d+) (-) "(.*?)" "(.*?)" (.*?)\s')


def process_log(log_file: Path) -> tuple[set[str], list[LogEntry], list[LogEntry]]:
    """
    Function processes the log file for each web site.

    :param log_file: Path of logfile
    :return: tuple of unique ips and LogEntrys from PUBLIC and SOHO
    """
    site_log_entries: list = []
    site_my_log_entries: list = []
    site_sources: set = set()

    site_long_files = 0
    unmatched = 0
    matched = 0

    with open(f"{log_file}") as logs:
        for log in logs:
            match = weblog_pattern.match(log)
            
            if match:
                matched += 1
                ip_address = match.group(1)
                timestamp = match.group(2)
                request = match.group(3)
                status_code = match.group(4)
                bytes_sent = match.group(5)
                referrer = match.group(6)
                user_agent_data = match.group(7)
                site = match.group(8)

                # skip parsing system cron jobs performed on bluehost server
                if ip_address == f"{my_secrets.my_bluehost_ip}":
                    continue

                site_sources.add(ip_address)

                if ":" in ip_address:
                    logger.warning(f"IPv6: {log}")
                    continue

                try:
                    user_agent = user_agent_data.split(" ")[0].strip()
                    client_os = (
                        user_agent_data.split(" ")[1].replace("(", "").replace(";", "")
                    )
                    client_version = user_agent_data.split(" ")[2:6]
                    client_version = " ".join(
                        [c.replace(";", "") for c in client_version]
                    )
                    client_version = "".join(
                        [c.replace(")", "") for c in client_version]
                    )

                    client = client_os + client_version

                except IndexError:
                    user_agent = "NA"
                    client = "NA"

                method, file, http_type = request.split()
                http_type = http_type.replace("')", "")
                file = file.replace("'[0]", "")

                site_sources.add(ip_address)

                entry: LogEntry = LogEntry(
                    server_timestamp=timestamp,
                    SOURCE=ip_address,
                    METHOD=method,
                    FILE=file,
                    HTTP=http_type,
                    REFERRER=referrer,
                    RESPONSE=status_code,
                    SIZE=bytes_sent,
                    AGENT=user_agent,
                    CLIENT=client,
                    SITE=site,
                )

                if ip_address == my_secrets.my_home_ip:
                    site_my_log_entries.append(entry)

                elif ip_address != my_secrets.my_home_ip:
                    site_log_entries.append(entry)
            else:
                unmatched += 1
                match = weblog_pattern_no_match.match(log)

                try:
                    unmatched -= 1
                    ip_address = match.group(1)
                    timestamp = match.group(2)
                    request = match.group(3)
                    status_code = match.group(4)
                    bytes_sent = match.group(5)
                    referrer = match.group(6)
                    user_agent_data = match.group(7)
                    site = match.group(8)

                    # skip parsing system cron jobs performed on bluehost server
                    if ip_address == f"{my_secrets.my_bluehost_ip}":
                        continue

                    site_sources.add(ip_address)

                    if ":" in ip_address:
                        logger.warning(f"IPv6: {log}")
                        continue

                    try:
                        user_agent = user_agent_data.split(" ")[0].strip()
                        client_os = (
                            user_agent_data.split(" ")[1].replace("(", "").replace(";", "")
                        )
                        client_version = user_agent_data.split(" ")[2:6]
                        client_version = " ".join(
                            [c.replace(";", "") for c in client_version]
                        )
                        client_version = "".join(
                            [c.replace(")", "") for c in client_version]
                        )

                        client = client_os + client_version

                    except IndexError:
                        user_agent = "NA"
                        client = "NA"

                    method, file, http_type = request.split()
                    http_type = http_type.replace("')", "")
                    file = file.replace("'[0]", "")

                    site_sources.add(ip_address)

                    entry: LogEntry = LogEntry(
                        server_timestamp=timestamp,
                        SOURCE=ip_address,
                        METHOD=method,
                        FILE=file,
                        HTTP=http_type,
                        REFERRER=referrer,
                        RESPONSE=status_code,
                        SIZE=bytes_sent,
                        AGENT=user_agent,
                        CLIENT=client,
                        SITE=site,
                    )

                    if ip_address == my_secrets.my_home_ip:
                        site_my_log_entries.append(entry)

                    elif ip_address != my_secrets.my_home_ip:
                        site_log_entries.append(entry)

                except:
                    logger.warning(f"still no re match: {log}")
                    unmatched +=1

        print(f"{log_file.name}: {unmatched=} {matched=}")

    logger.info(
        f"\t\t{len(site_log_entries)} PUBLIC logs with {len(set(site_sources))} unique source ip"
    )
    logger.info(f"\t\t{len(site_my_log_entries)} SOHO logs")
    logger.info(
        f"\t\t{len(site_log_entries) + len(site_my_log_entries)} SITE LOG ENTRIES"
    )

    if site_long_files >= 1:
        logger.warning(f"\t\t{site_long_files} long file names encountered.")

    return site_sources, site_log_entries, site_my_log_entries


def start_processing(
    log_paths: list[Path], month_name_abbr: str | None, year_2_str: str | None
) -> tuple[list[str], list[LogEntry], list[LogEntry]]:
    """
    Function processes all current production website access logs.

    :param log_paths: list of Paths pointing to unzipped logfiles
    :param month_name: abbreciated month name
    :param year: year as str
    :return: tuple of ip addresses, ny LogEntry, other LogEntry
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
            logger.info(f"Parsing {p.name} logs")
            sources, public_logs, soho_logs = process_log(p)
            all_sources.extend(sources)
            all_public_log_entries.extend(public_logs)
            all_soho_log_entries.extend(soho_logs)

    if all_long_files > 0:
        logger.warning(
            f"\tLOG ENTRIES OVER 120 characers (all-sites) = {all_long_files}"
        )

    logger.info("COMPLETED WEBLOG PARSING")
    return all_sources, all_public_log_entries, all_soho_log_entries
