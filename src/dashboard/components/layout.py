from dash import Dash, html  # , dash_table
# from dashboard.components import (
# bar_chart,
# nation_dropdown,
# month_dropdown,
# pie_chart,
# category_dropdown,
# year_dropdown,
# )

# from ..data.source import DataSource


def create_layout(app: Dash) -> html.Div:
    return (
        html.Div(
            className="app-div",
            children=[
                html.H1(app.title),
                html.Hr(),
                html.Div(
                    className="dropdown-container",
                    children=[
                        # nation_dropdown.render(app),
                        # year_dropdown.render(app),
                        # month_dropdown.render(app),
                        # category_dropdown.render(app),
                    ],
                ),
            ],
        ),
    )
    # bar_chart.render(app, source),
    #     pie_chart.render(app, source),
    #     ],
    # )


# app.layout = dbc.Alert(
#     "Hello, Bootstrap!", className="m-5"
# )
