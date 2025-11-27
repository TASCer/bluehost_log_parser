import logging

from pathlib import Path
from bluehost_log_parser.my_secrets import local_dburi
from sqlalchemy import create_engine, exc, text, Engine
from logging import Logger

logger: Logger = logging.getLogger(__name__)

COUNTRY_SEED_DATA: Path = Path.cwd().parent.parent / "misc" / "countries.txt"


def countries() -> None:
    try:
        engine: Engine = create_engine(f"mysql+pymysql://{local_dburi}")

    except (exc.SQLAlchemyError, exc.OperationalError) as e:
        logger.critical(str(e))

    with open(Path.cwd().parent.parent / "misc" / "countries.txt") as fh:
        data: list[str] = fh.readlines()

    with engine.connect() as conn, conn.begin():
        for c in data:
            country: list[str] = c.rstrip().split("\t")
            name, alpha2, alpha3, number = country

            if "'" in name:
                name: str = name.replace("'", "''")

            conn.execute(
                text(
                    f"""INSERT IGNORE into countries values('{name}', '{alpha2}', '{alpha3}', '{number}');"""
                )
            )


if __name__ == "__main__":
    countries()
