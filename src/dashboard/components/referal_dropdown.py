from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids
# from .dropdown_helper import to_dropdown_options


def render(app: Dash, data: DataFrame) -> html.Div:
    @app.callback(
        Output(ids.REFERAL_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            # Input(ids.SELECT_ALL_CODES_BUTTON, "n_clicks"),
            Input(ids.SELECT_ALL_REFERALS_BUTTON, "n_clicks"),

        ],
    )
    def select_all_referals(years: list[str], months: list[str], _: int) -> list[str]:
        return data["REF_URL"].unique()

    return html.Div(
        children=[
            html.H6("general.referal"),
            dcc.Dropdown(
                id=ids.REFERAL_DROPDOWN,
                options=data["REF_URL"].unique(),
                value=data["REF_URL"].unique(),
                multi=True,
                placeholder="general.select",
            ),
            html.Button(
                className="dropdown-button",
                children="general.select_all",
                id=ids.SELECT_ALL_REFERALS_BUTTON,
                n_clicks=0,
            ),
        ],
    )
