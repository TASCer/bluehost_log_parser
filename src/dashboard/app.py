import dash_bootstrap_components as dbc
import datetime as dt
import logging

from dash import Dash
from dashboard.components import layout
from dashboard.data.loader import load_weblog_data
from logging import Formatter, Logger
from pandas import DataFrame
from pathlib import Path

LOGGER_ROOT = Path.cwd().parent
now: dt = dt.date.today()
todays_date: str = now.strftime("%D").replace("/", "-")

dash_logger: Logger = logging.getLogger()
dash_logger.setLevel(logging.INFO)

fh = logging.FileHandler(f"{LOGGER_ROOT}/dashboard-{todays_date}.log")
fh.setLevel(logging.DEBUG)

formatter: Formatter = logging.Formatter(
    "%(asctime)s - %(filename)s -%(lineno)d - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)

dash_logger.addHandler(fh)

logger: Logger = logging.getLogger(__name__)

app = Dash(
    name="WebLog App",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    description="View Apache Weblog data",
    title="Bluehost Weblogs",
)


def main():
    source: DataFrame = load_weblog_data()
    logger.info("LOADED SOURCE DATA")
    app.layout = layout.create_layout(app, data=source)

    app.run(debug=True, port="8000")


if __name__ == "__main__":
    main()
