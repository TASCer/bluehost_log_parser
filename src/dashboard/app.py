import datetime as dt
import logging

import dash_bootstrap_components as dbc

from dash import Dash
from dashboard.data.loader import load_weblog_data
from logging import Formatter, Logger
from pathlib import Path
from dashboard.components import layout

LOGGER_ROOT = Path.cwd().parent
now: dt = dt.date.today()
todays_date: str = now.strftime("%D").replace("/", "-")

root_logger: Logger = logging.getLogger()
root_logger.setLevel(logging.INFO)

fh = logging.FileHandler(f"{LOGGER_ROOT}/dashboard-{todays_date}.log")
fh.setLevel(logging.DEBUG)

formatter: Formatter = logging.Formatter(
    "%(asctime)s - %(filename)s -%(lineno)d - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)

root_logger.addHandler(fh)

logger: Logger = logging.getLogger(__name__)

app = Dash(
    name="WebLog App",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    description="View Apache Weblog data",
    title="Weblog App",
)


def main():
    data = load_weblog_data()

    app.layout = layout.create_layout(app, source=data)

    app.run(debug=True)


if __name__ == "__main__":
    main()
