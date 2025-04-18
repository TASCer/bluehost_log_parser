import babel.dates
import datetime as dt
import i18n
import pandas as pd

from bluehost_log_parser.my_secrets import local_dburi
from functools import partial, reduce
from typing import Callable
from sqlalchemy import Engine, create_engine, exc

class DataSchema:
    AMOUNT = "amount"
    CATEGORY = "category"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"

try:
    engine: Engine = create_engine(f"mysql+pymysql://{local_dburi}")

except exc.SQLAlchemyError as e:
    # logger.critical(str(e))
    exit()



Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]



def create_year_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.YEAR] = df[DataSchema.DATE].dt.year.astype(str)
    return df


def create_month_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.MONTH] = df[DataSchema.DATE].dt.month.astype(str)
    return df


def convert_date_locale(df: pd.DataFrame, locale: str) -> pd.DataFrame:
    def date_repr(date: dt.date) -> str:
        return babel.dates.format_date(date, format="MMMM", locale=locale)

    df[DataSchema.MONTH] = df[DataSchema.DATE].apply(date_repr)
    return df


def translate_category_language(df: pd.DataFrame) -> pd.DataFrame:
    def translate(category: str) -> str:
        return i18n.t(f"category.{category}")

    df[DataSchema.CATEGORY] = df[DataSchema.CATEGORY].apply(translate)
    return df


def compose(*functions: Preprocessor) -> Preprocessor:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)


def load_weblog_data(locale: str) -> pd.DataFrame:
    with engine.connect() as conn, conn.begin():
        data = pd.read_sql(sql="SELECT * from logs", con=conn)#,
        
    preprocessor = compose(
        create_year_column,
        create_month_column,
        partial(convert_date_locale, locale=locale),
        translate_category_language,
    )
    return preprocessor(data)
