import country_converter as coco
import datetime as dt
import ipwhois
import logging
import my_secrets

from ipwhois import IPWhois
from logging import Logger
from sqlalchemy.engine import Engine, CursorResult
from sqlalchemy import exc, create_engine, text
from typing import Optional

# SQL TABLES
LOGS = "logs"
SOURCES = "sources"


def lookup():
    """
    Updates lookup table 'sources' entries with full country name and ASN Description from whois
    """
    logger: Logger = logging.getLogger(__name__)
    start_time = dt.datetime.utcnow()

    http_errors = 0

    try:
        engine: Engine = create_engine(
            f"mysql+pymysql://{my_secrets.dbuser}:{my_secrets.dbpass}@{my_secrets.dbhost}/{my_secrets.dbname}"
        )

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        exit()

    with engine.connect() as conn, conn.begin():
        logger.info(
            "Updating lookup table with source country name and description via IPWhois"
        )

        errors = 0

        try:
            sql_no_country: CursorResult = conn.execute(
                text(
                    f"""SELECT * from {SOURCES} WHERE COUNTRY = '' or COUNTRY is null or country like '%HTTP%';"""
                )
            )

            no_country: list = [i for i in sql_no_country]

        except exc.SQLAlchemyError as e:
            logger.warning(str(e))

        for ip, country, code, desc in no_country:
            # if ip == '2a06:98c0:3600:':
            #     logger.warning("IPv6 found {ip}")
            #     continu
            
            try:
                obj: IPWhois = ipwhois.IPWhois(ip, timeout=10)
                result: dict = obj.lookup_rdap()

            except ipwhois.HTTPLookupError as http:
                http_errors += 1
                http: str = str(http).split("&")[0]
                conn.execute(
                    text(
                        f"""update {SOURCES} SET country = '{str(http)}' WHERE SOURCE = '{ip}';"""
                    )
                )

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

                conn.execute(
                    text(
                        f"""update {SOURCES} SET country = '{error}' WHERE SOURCE = '{ip}';"""
                    )
                )

                continue

            asn_description: str = result["asn_description"]

            if asn_description == "NA" or asn_description is None:
                asn_description = "NA"
            else:
                asn_description = asn_description.rsplit(",")[0]

            if result["asn_country_code"] is None:
                logger.warning(f"{ip} had no alpha2 code, setting country name to '00'")
                asn_alpha2: str = "00"
                conn.execute(
                    text(
                        f"""update {SOURCES} SET country = '{asn_alpha2}' WHERE SOURCE = '{ip}';"""
                    )
                )
                continue

            elif result["asn_country_code"].islower():
                asn_alpha2: str = asn_alpha2.upper()
                logger.warning(
                    f"RDAP responded with lowercase country for {ip}, should be upper"
                )

            else:
                asn_alpha2 = result["asn_country_code"]
                country_name: Optional[str] = coco.convert(asn_alpha2)

            try:
                conn.execute(
                    text(f"""UPDATE `{my_secrets.dbname}`.`{SOURCES}`
                        SET
                            `COUNTRY` = '{country_name}',
                            `ALPHA2` = '{asn_alpha2}',
                            `DESCRIPTION` = '{asn_description}'
                        WHERE `SOURCE` = '{ip}';""")
                )
            except exc.ProgrammingError as e:
                logger.error(e)

    if errors >= 1:
        logger.warning(f"sources table: {errors} errors encountered")

    logger.info(
        f"sources table: {len(no_country) - errors} updated with country names and ASN description."
    )

    stop_time = dt.datetime.utcnow()
    elapsed_time = int((stop_time - start_time).total_seconds())

    logger.info(f"\tupdated: {len(no_country)} lookups in {elapsed_time} seconds.")

    if elapsed_time >= 60:
        minutes: int = elapsed_time // 60
        whois_rate: int = len(no_country) // minutes
        logger.info(f"\t ~{whois_rate= } lookups per minute")


if __name__ == "__main__":
    lookup()
