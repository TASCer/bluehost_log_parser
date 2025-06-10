import dash
from dash import html  # , dcc, callback, Input, Output
from dashboard.components import map_viewer
from pandas import DataFrame
from dashboard.data import loader

dash.register_page(__name__)

source: DataFrame = loader.load_weblog_data()

layout = html.Div(
    html.Div(
        className="container-fluid",
        children=[
            html.Hr(),
            map_viewer.render(source),
        ],
    )
)
