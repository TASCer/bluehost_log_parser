from venv import logger
from dash import Dash, dash_table, html, dcc
from dashboard.components import (
    bar_chart,
    code_dropdown,
    month_dropdown,
    pie_chart,
    referral_dropdown,
    year_dropdown,
    table_viewer,
)
from pandas import DataFrame


def create_layout(app: Dash, data: DataFrame) -> html.Div:
    logger.info(f"LAYOUT CREATED df:{len(data)}")

    return html.Div(
        className="container-fluid",
        children=[
            html.P(f"SOURCE WEBLOG COUNT: {len(data)}"),
            # html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown-button",
                children=[
                    year_dropdown.render(app, data),
                    month_dropdown.render(app, data),
                    code_dropdown.render(app, data),
                    referral_dropdown.render(app, data),
                    table_viewer.render(app, data),
                ],
            ),
            bar_chart.render(app, data),
            pie_chart.render(app, data),
        ],
    )
