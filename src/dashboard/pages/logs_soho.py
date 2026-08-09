import dash
from dash import html
from pandas import DataFrame

from dashboard.components import log_viewer_soho
from dashboard.data import loader

dash.register_page(__name__, path="/soho")


source: DataFrame = loader.load_soho_weblog_data()

layout = html.Div(
    [
        html.Div(
            children=[
                log_viewer_soho.render(source),
            ],
        ),
    ]
)
