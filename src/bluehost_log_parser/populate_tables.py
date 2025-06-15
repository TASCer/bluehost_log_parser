import logging

from sqlalchemy import create_engine, exc, text
from logging import Logger
from bluehost_log_parser.db_checks import COUNTRIES_TABLE
from bluehost_log_parser.my_secrets import local_dburi


logger: Logger = logging.getLogger(__name__)


def countries():
    try:
        engine = create_engine(f"mysql+pymysql://{local_dburi}")

    except (exc.SQLAlchemyError, exc.OperationalError) as e:
        logger.critical(str(e))
        return False

    with open("../../misc/countries.txt") as fh:
        data = fh.readlines()

    with engine.connect() as conn, conn.begin():
        for c in data:
            country = c.rstrip().split("\t")
            name, alpha2, alpha, number = country

            if "'" in name:
                name = name.replace("'", "''")

            print(name, alpha, alpha2, number)
            conn.execute(
                text(
                    f"""INSERT IGNORE into {COUNTRIES_TABLE} values('{name}', '{alpha}', '{alpha2}', '{number}');"""
                )
            )


if __name__ == "__main__":
    countries()
