from dash import Dash, dash_table, html, dcc
from dashboard.components import (
    bar_chart,
    code_dropdown,
    month_dropdown,
    pie_chart,
    year_dropdown,
)
from pandas import DataFrame


def create_layout(app: Dash, data: DataFrame) -> html.Div:
    return html.Div(
        className="bg-primary-subtle border border-primary-subtle p-2",
        children=[
            html.P(len(data)),
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[
                    year_dropdown.render(app, data),
                    month_dropdown.render(app, data),
                    code_dropdown.render(app, data),
                ],
            ),
            bar_chart.render(app, data),
            # pie_chart.render(app, data),
        ],
    )
