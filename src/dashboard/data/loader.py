import logging
import pandas as pd
from functools import reduce
from typing import Callable
from sqlalchemy import create_engine, Engine, exc
from bluehost_log_parser.my_secrets import local_dburi
from logging import Logger

logger: Logger = logging.getLogger(__name__)

Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]


def create_year_column(df: pd.DataFrame) -> pd.DataFrame:
    df["YEAR"] = df["ACCESSED"].dt.year
    return df


def create_month_column(df: pd.DataFrame) -> pd.DataFrame:
    df["MONTH"] = df["ACCESSED"].dt.month
    return df


def compose(*functions: Preprocessor) -> Preprocessor:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


def load_weblog_data() -> pd.DataFrame:
    try:
        engine: Engine = create_engine(f"mysql+pymysql://{local_dburi}")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        exit()

    data = pd.read_sql_table(con=engine.connect(), table_name="logs")

    preprocessor = compose(
        create_year_column,
        create_month_column,
    )

    return preprocessor(data)
