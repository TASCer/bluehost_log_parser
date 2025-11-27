import dash
import dash_bootstrap_components as dbc
import datetime as dt
import logging

from dash import Dash, dcc, html

from logging import Logger, Formatter

from bluehost_log_parser.main import LOGGER_ROOT
from bluehost_log_parser import db_checks

now = dt.date.today()
todays_date: str = now.strftime("%D").replace("/", "-")

logger: Logger = logging.getLogger()
logger.setLevel(logging.INFO)

logger: Logger = logging.getLogger(__name__)
fh = logging.FileHandler(f"{LOGGER_ROOT}/{todays_date}.log")
fh.setLevel(logging.DEBUG)

formatter: Formatter = logging.Formatter(
    "%(asctime)s - %(filename)s -%(lineno)d - %(levelname)s - %(message)s"
)
fh.setFormatter(formatter)

logger.addHandler(fh)

logger: Logger = logging.getLogger(__name__)

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    description="View Apache Weblog data",
    title="Analyze Weblogs",
    use_pages=True,
)


app.layout = html.Div(
    [
        # html.H1("Bluehost Log Analysis"),
        html.Div(
            [
                html.Div(
                    dcc.Link(
                        f"{page['name']} - {page['path']}",
                        href=page["relative_path"],
                    )
                )
                for page in dash.page_registry.values()
            ]
        ),
        dash.page_container,
    ]
)


if __name__ == "__main__":
    if db_checks.tables():
        app.run(debug=True, port="8000")
    else:
        logger.error("NO DATABASE TABLES FOUND")
