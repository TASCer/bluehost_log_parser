from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids
from .dropdown_helper import to_dropdown_options


def render(app: Dash, source: DataFrame) -> html.Div:
    @app.callback(
        Output(ids.CODE_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_CODES_BUTTON, "n_clicks"),
        ],
    )
    def select_all_codes(years: list[str], months: list[str], _: int) -> list[str]:
        return source.filter(source["YEAR"].unique(), source["MONTH"].unique())

    return html.Div(
        children=[
            html.H6("general.code"),
            dcc.Dropdown(
                id=ids.CODE_DROPDOWN,
                options=to_dropdown_options(source["CODE"].unique()),
                value=source["CODE"].unique(),
                multi=True,
                placeholder="general.select",
            ),
            html.Button(
                className="dropdown-button",
                children="general.select_all",
                id=ids.SELECT_ALL_CODES_BUTTON,
                n_clicks=0,
            ),
        ],
    )
