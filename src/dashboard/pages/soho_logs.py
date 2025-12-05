import dash
from dash import html
from dashboard.components import soho_log_viewer
from dashboard.data import loader
from pandas import DataFrame

dash.register_page(__name__, path="/soho")


source: DataFrame = loader.load_soho_weblog_data()

layout = html.Div(
    [
        html.Div(
            children=[
                soho_log_viewer.render(source),
            ],
        ),
    ]
)
