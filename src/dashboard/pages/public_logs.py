import dash
from dash import html
from dashboard.components import public_log_viewer
from dashboard.data import loader
from pandas import DataFrame

dash.register_page(__name__, path="/")


source: DataFrame = loader.load_public_weblog_data()

layout = html.Div(
    [
        html.Div(
            children=[
                public_log_viewer.render(source),
            ],
        ),
    ]
)
