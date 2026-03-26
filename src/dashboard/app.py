# TODO add cache https://github.com/AnnMarieW/dash-multi-page-app-demos/blob/main/multi_page_store/app.py
import dash
import dash_bootstrap_components as dbc
import datetime as dt
import logging

from bluehost_log_parser.main import LOGGER_ROOT
from bluehost_log_parser.database import db_checks
from dash import Dash, dcc, html
from flask_caching import Cache
from logging import Logger, Formatter


todays_date: str = dt.date.today().strftime("%D").replace("/", "-")

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
    description="View and Analyze Apache Weblog data",
    title="Analyze Weblogs",
    use_pages=True,
)

# cache = Cache(app.server, config={"CACHE_TYPE": "filesystem", "CACHE_DIR": "./data/flask_cache"})


app.layout = html.Div(
    [
        # dcc.Store(id="store", data={}),
        html.H1("WEBLOG Multi Page Viewer App Demo"),
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
