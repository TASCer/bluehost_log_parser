# TODO IMPLEMENT THE dropdown helper?
from dash import dcc, html, callback
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids
# from .dropdown_helper import to_dropdown_options


def render(source: DataFrame) -> html.Div:
    all_responses: list[str] = source["RESPONSE"].tolist()
    unique_responses: list[str] = sorted(set(all_responses))

    @callback(
        Output(ids.RESPONSE_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_RESPONSES_BUTTON, "n_clicks"),
        ],
    )
    def select_all_codes(years: list[str], months: list[str], _: int) -> list[str]:
        return unique_responses

    return html.Div(
        children=[
            html.H6("response"),
            dcc.Dropdown(
                id=ids.RESPONSE_DROPDOWN,
                options=unique_responses,
                value=unique_responses,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children="all_responses",
                id=ids.SELECT_ALL_RESPONSES_BUTTON,
                n_clicks=0,
            ),
        ],
    )
