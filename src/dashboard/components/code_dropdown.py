from dash import dcc, html, callback
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids
# from .dropdown_helper import to_dropdown_options


def render(source: DataFrame) -> html.Div:
    all_codes: list[str] = source["CODE"].tolist()
    unique_codes = sorted(set(all_codes))

    @callback(
        Output(ids.CODE_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_CODES_BUTTON, "n_clicks"),
        ],
    )
    def select_all_codes(years: list[str], months: list[str], _: int) -> list[str]:
        return unique_codes

    return html.Div(
        children=[
            html.H6("response.code"),
            dcc.Dropdown(
                id=ids.CODE_DROPDOWN,
                options=unique_codes,
                value=unique_codes,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children="all_codes",
                id=ids.SELECT_ALL_CODES_BUTTON,
                n_clicks=0,
            ),
        ],
    )
