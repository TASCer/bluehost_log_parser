import pandas as pd
from sqlalchemy import create_engine, Engine, exc
from bluehost_log_parser.my_secrets import local_dburi


class DataSchema:
    # AMOUNT = "amount"
    # CATEGORY = "category"
    DATE = "date"
    MONTH = "month"
    YEAR = "year"


def create_year_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.YEAR] = df[DataSchema.DATE].dt.year.astype(str)
    return df


def create_month_column(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.MONTH] = df[DataSchema.DATE].dt.month.astype(str)
    return df


def load_weblog_data() -> pd.DataFrame:
    try:
        engine: Engine = create_engine(f"mysql+pymysql://{local_dburi}")

    except exc.SQLAlchemyError as e:
        # logger.critical(str(e))
        exit()

    df = pd.read_sql_table(
        con=engine.connect(), table_name="logs", parse_dates=[DataSchema.DATE]
    )
    print(df.info())
    return df
