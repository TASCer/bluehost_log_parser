# https://dash.plotly.com/urls
import dash_bootstrap_components as dbc
import datetime as dt
import logging

from dash import Dash
from dashboard.components import layout
from dashboard.data.loader import load_weblog_data
from logging import Logger
from pandas import DataFrame

now: dt = dt.date.today()
todays_date: str = now.strftime("%D").replace("/", "-")

dash_logger: Logger = logging.getLogger()
dash_logger.setLevel(logging.INFO)

logger: Logger = logging.getLogger(__name__)

app = Dash(
    name="WebLog App",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    description="View Apache Weblog data",
    title="Bluehost Weblogs",
    use_pages=False,
)


def main() -> None:
    source: DataFrame = load_weblog_data()
    logger.info("LOADED SOURCE DATA")
    app.layout = layout.create_layout(app, data=source)

    app.run(debug=True, port="8000")


if __name__ == "__main__":
    main()
