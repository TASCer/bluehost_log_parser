# TODO rework database activity for use in dropdowns?

import logging
import pandas as pd

from bluehost_log_parser.my_secrets import local_dburi
from functools import reduce
from typing import Callable
from sqlalchemy import Engine, create_engine, exc
from logging import Logger
from pandas import DataFrame

logger: Logger = logging.getLogger(__name__)

try:
    engine: Engine = create_engine(f"mysql+pymysql://{local_dburi}")

except exc.SQLAlchemyError as e:
    logger.critical(str(e))
    exit()

Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]


def create_year_column(df: pd.DataFrame) -> pd.DataFrame:
    df["YEAR"] = df["ACCESSED"].dt.year.astype(str)
    return df


def split_timestamp(df: pd.DataFrame) -> pd.DataFrame:
    df["DATE"] = df["ACCESSED"].dt.date
    df["TIME"] = df["ACCESSED"].dt.time

    return df


def create_month_column(df: pd.DataFrame) -> pd.DataFrame:
    df["MONTH"] = df["ACCESSED"].dt.strftime("%B")
    return df


def compose(*functions: Preprocessor) -> Preprocessor:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


def load_weblog_data() -> pd.DataFrame:
    with engine.connect() as conn, conn.begin():
        data: DataFrame = pd.read_sql(
            sql="""SELECT l.*, s.COUNTRY, s.ALPHA2 , s.ALPHA3 FROM `bluehost-weblogs`.public_logs l join sources s on l.SOURCE = s.SOURCE;""",
            con=conn,
        )
    preprocessor = compose(
        split_timestamp,
        create_year_column,
        create_month_column,
    )

    logger.info(f"{len(data)=}")

    return preprocessor(data)
