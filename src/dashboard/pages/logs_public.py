import dash
from dash import html
from pandas import DataFrame

from dashboard.components import log_viewer_public
from dashboard.data import loader

dash.register_page(__name__, path="/")


source: DataFrame = loader.load_public_weblog_data()

layout = html.Div(
    [
        html.Div(
            children=[
                log_viewer_public.render(source),
            ],
        ),
    ]
)
