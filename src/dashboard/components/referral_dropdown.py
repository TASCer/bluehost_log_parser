from dash import dcc, html, callback
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids
# from .dropdown_helper import to_dropdown_options


def render(data: DataFrame) -> html.Div:
    all_referrers: list[str] = data["REFERRER"].tolist()
    unique_referrers = sorted(set(all_referrers))

    @callback(
        Output(ids.REFERRER_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.RESPONSE_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_REFERRERS_BUTTON, "n_clicks"),
        ],
    )
    def select_all_referals(
        years: list[str], months: list[str], codes: list[str], _: int
    ) -> list[str]:
        return unique_referrers

    return html.Div(
        children=[
            html.H6("referral.url"),
            dcc.Dropdown(
                id=ids.REFERRER_DROPDOWN,
                options=unique_referrers[:10],
                value=None,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children="all_referrers",
                id=ids.SELECT_ALL_REFERRERS_BUTTON,
                n_clicks=0,
            ),
        ],
    )
