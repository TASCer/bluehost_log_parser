from dash import Dash, dash_table, html, dcc
from dashboard.components import (
    bar_chart,
    code_dropdown,
    month_dropdown,
    pie_chart,
    year_dropdown,
)
from pandas import DataFrame

def create_layout(app: Dash, source: DataFrame) -> html.Div:
    return html.Div(
        className="bg-primary-subtle border border-primary-subtle p-2",
        children=[
            html.P(source.columns),
            html.H1(app.title),
            html.Hr(),
            # html.H6(source.unique_years),
            html.Div(
                className="dropdown-container",
                children=[
                    year_dropdown.render(app, source),
                    month_dropdown.render(app, source),
                    code_dropdown.render(app, source),
                ],
            ),
            bar_chart.render(app, source),
            pie_chart.render(app, source),
        ],
    )
