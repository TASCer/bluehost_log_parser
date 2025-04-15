# https://github.com/ArjanCodes/2022-dash
import datetime as dt
import logging
import plotly.express as px
import dash_bootstrap_components as dbc
# import datetime as dt

from dash import Dash
from dashboard.data import loader
from logging import Formatter, Logger
from pathlib import Path

# from dash.dependencies import Input, Output
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
)


def main():
    df = loader.load_weblog_data()
    # df.where((df["CODE"] == "200") & (df["REF_URL"] == "TASCS.NET"), inplace=True)
    # df.sort_values("ACCESSED", inplace=True, ascending=False)
    # print("DF", df.info())
    df_group = df.groupby("REF_URL").count()
    print(df_group)
    refs = [r.lower() for r in df_group]
    print("REF", refs, len(refs))

    app.layout = layout.create_layout(app, df)
    print(app.layout)
    # app.layout = [
    # dcc.Graph(figure=px.histogram(df, x="AGENT", y="SIZE", histfunc="avg")),
    # ]

    app.run(debug=True)


if __name__ == "__main__":
    main()
