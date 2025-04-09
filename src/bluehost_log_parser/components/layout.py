from dash import Dash, html, dash_table
from bluehost_log_parser.components import (
    # bar_chart,
    category_dropdown,
    # month_dropdown,
    # pie_chart,
    # year_dropdown,
)

# from ..data.source import DataSource


def create_layout(app: Dash, source) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            dash_table.DataTable(data=source.to_dict("records"), page_size=25),

            # html.Div(
            #     className="dropdown-container",
            #     # children=[
                    # year_dropdown.render(app, source),
                    # month_dropdown.render(app, source),
                    # category_dropdown.render(app, source),
                ],
            ),
        #     bar_chart.render(app, source),
        #     pie_chart.render(app, source),
    #     ],
    # )
