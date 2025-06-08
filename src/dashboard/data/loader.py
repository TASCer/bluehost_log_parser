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


def create_month_column(df: pd.DataFrame) -> pd.DataFrame:
    df["MONTH"] = df["ACCESSED"].dt.strftime("%B")
    return df


def compose(*functions: Preprocessor) -> Preprocessor:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


def load_weblog_data() -> pd.DataFrame:
    with engine.connect() as conn, conn.begin():
        data: DataFrame = pd.read_sql(
            sql="""SELECT * FROM `bluehost-weblogs`.logs where ACCESSED like '2025-06-%%';""",
            con=conn,
        )
    # where ACCESSED like '2025-04%%'
    preprocessor = compose(
        create_year_column,
        create_month_column,
    )
    return preprocessor(data)
