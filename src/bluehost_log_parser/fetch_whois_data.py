import country_converter as coco
import datetime as dt
import ipwhois
import logging

from datetime import datetime
from ipwhois import IPWhois
from logging import Logger
from typing import Optional

SOURCES_TABLE = "sources"

logger: Logger = logging.getLogger(__name__)

now: dt = dt.date.today()


def get_country(source_ips: list) -> list[str]:
    http_errors = 0
    whois_results: list = []
    start_time: datetime = dt.datetime.utcnow()

    for ip in source_ips:
        try:
            obj: IPWhois = ipwhois.IPWhois(ip, timeout=10)
            result: dict = obj.lookup_rdap()

        except ipwhois.HTTPLookupError as http:
            http_errors += 1
            http: str = str(http).split("&")[0]

            continue

        except ipwhois.ASNParseError as parse_err:
            logger.error(parse_err)
            print(parse_err)

        except (
            UnboundLocalError,
            ValueError,
            AttributeError,
            ipwhois.BaseIpwhoisException,
            ipwhois.ASNLookupError,
            ipwhois.ASNOriginLookupError,
            ipwhois.ASNRegistryError,
            ipwhois.HostLookupError,
            ipwhois.HTTPLookupError,
        ) as e:
            error: str = str(e).split("http:")[0]
            print(f"Non httplookup error: {error} {ip}")
            logger.warning(f"Non httplookup error: {error} {ip}")

            continue

        asn_description: str = result["asn_description"]

        if asn_description == "NA" or asn_description is None:
            asn_description = "NA"
        else:
            asn_description: str = asn_description.rsplit(",")[0]

        if result["asn_country_code"] is None:
            logger.warning(f"{ip} had no alpha2 code, setting country name to '00'")
            asn_alpha2: str = "00"

            continue

        elif result["asn_country_code"].islower():
            asn_alpha2: str = asn_alpha2.upper()
            logger.warning(
                f"RDAP responded with lowercase country for {ip}, should be upper"
            )

        else:
            asn_alpha2: str = result["asn_country_code"]
            country_name: Optional[str] = coco.convert(asn_alpha2, to="name")

        whois_results.append([ip, country_name, asn_alpha2, asn_description])

    stop_time = dt.datetime.utcnow()
    elapsed_time: int = int((stop_time - start_time).total_seconds())

    logger.info(
        f"\tqueried: {len(source_ips)} source country names and descriptions in {elapsed_time} seconds."
    )

    if elapsed_time >= 60:
        minutes: int = elapsed_time // 60
        whois_rate: int = len(source_ips) // minutes
        logger.info(f"\t ~{whois_rate= } lookups per minute")

    return whois_results
