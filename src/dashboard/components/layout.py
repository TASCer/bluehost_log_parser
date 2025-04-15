from dash import Dash, html, dash_table, dcc
import plotly.express as px
import dash_bootstrap_components as dbc
from dashboard.components import (
    # bar_chart,
    # nation_dropdown,
    # month_dropdown,
    # pie_chart,
    category_dropdown,
    # year_dropdown,
)

# from ..data.source import DataSource


def create_layout(app: Dash, data) -> html.Div:
    return (
        dbc.Alert("WebLogs App", className="s-15"),
        # ISSUE USING COLUMN SELECTABLE. NEED TO USE DataSource method DF not supported.
        dash_table.DataTable(
            data=data.to_dict("records"), page_size=25, column_selectable=False
        ),
        html.Div(
            className="app-div",
            children=[
                # html.H1(app.title),
                html.Hr(),
                dcc.Graph(
                    figure=px.histogram(data, x="AGENT", y="SIZE", histfunc="avg")
                ),
                html.Div(
                    className="dropdown-container",
                    children=[
                        # nation_dropdown.render(app),
                        # year_dropdown.render(app),
                        # month_dropdown.render(app),
                        category_dropdown.render(app),
                    ],
                ),
            ],
        ),
    )
    # bar_chart.render(app, source),
    #     pie_chart.render(app, source),
    #     ],
    # )
