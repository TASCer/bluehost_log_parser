import logging

from sqlalchemy import create_engine, exc, text, Engine
from logging import Logger
from bluehost_log_parser.db_checks import COUNTRIES_TABLE
from bluehost_log_parser.my_secrets import local_dburi


logger: Logger = logging.getLogger(__name__)


def countries() -> None:
    try:
        engine: Engine = create_engine(f"mysql+pymysql://{local_dburi}")

    except (exc.SQLAlchemyError, exc.OperationalError) as e:
        logger.critical(str(e))

    with open("../../misc/countries.txt") as fh:
        data: list[str] = fh.readlines()

    with engine.connect() as conn, conn.begin():
        for c in data:
            country: list[str] = c.rstrip().split("\t")
            name, alpha2, alpha, number = country

            if "'" in name:
                name: str = name.replace("'", "''")

            conn.execute(
                text(
                    f"""INSERT IGNORE into {COUNTRIES_TABLE} values('{name}', '{alpha}', '{alpha2}', '{number}');"""
                )
            )


if __name__ == "__main__":
    countries()
