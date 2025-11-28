import dash
from dash import html
from dashboard.components import (
    bar_chart,
    month_dropdown,
    pie_chart,
    referral_dropdown,
    response_dropdown,
    year_dropdown,
    site_dropdown,
)
from pandas import DataFrame
from dashboard.data import loader

dash.register_page(__name__)

source: DataFrame = loader.load_weblog_data()

layout = html.Div(
    html.Div(
        className="container-fluid",
        children=[
            html.Hr(),
            html.Div(
                className="dropdown-button",
                children=[
                    year_dropdown.render(source),
                    month_dropdown.render(source),
                    response_dropdown.render(source),
                    referral_dropdown.render(source),
                    site_dropdown.render(source),
                ],
            ),
            bar_chart.render(source),
            pie_chart.render(source),
        ],
    )
)
