import datetime as dt
from datetime import date, datetime


def get_logger_date() -> str:
    """
    Function formats and returns today's date for logger name.

    """
    date_today: date = dt.date.today()
    todays_date: str = date_today.strftime("%D").replace("/", "-")

    return todays_date


def get_now() -> date:
    """
    Function creates and returns a date object for today.

    """
    return dt.date.today()


def get_monthname_short(arg_year: int, arg_month: int) -> str:
    """
    Function provides a 3-letter abbreviated month name.

    :param year: year int from argparse
    :param month: month int from argparse
    :return: short month name used for downkoading log files
    """
    arg_date: str = f"{arg_year}-{arg_month}-01"
    date_obj: datetime = dt.datetime.strptime(arg_date, "%Y-%m-%d")
    month_name_abbr: str = date_obj.strftime("%b")

    return month_name_abbr


print(get_logger_date())
print(get_now())
print(get_monthname_short(2025, 10))
