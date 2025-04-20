from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids
from .dropdown_helper import to_dropdown_options


def render(app: Dash, source: DataFrame) -> html.Div:
    @app.callback(
        Output(ids.YEAR_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_YEARS_BUTTON, "n_clicks"),
    )
    def select_all_years(_: int) -> list[str]:
        return source.unique_years

    return html.Div(
        children=[
            html.H6("general.year"),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=[{"label": year, "value": year} for year in source["YEAR"]],
                value=source["YEAR"],
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=["general.select_all"],
                id=ids.SELECT_ALL_YEARS_BUTTON,
                n_clicks=0,
            ),
        ]
    )
