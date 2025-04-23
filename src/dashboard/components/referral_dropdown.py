from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids
# from .dropdown_helper import to_dropdown_options


def render(app: Dash, data: DataFrame) -> html.Div:
    all_referrals: list[str] = data["REF_URL"].tolist()
    unique_referrals = sorted(set(all_referrals))

    @app.callback(
        Output(ids.REFERRAL_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CODE_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_REFERRALS_BUTTON, "n_clicks"),
        ],
    )
    def select_all_referals(
        years: list[str], months: list[str], codes: list[str], _: int
    ) -> list[str]:
        return unique_referrals

    return html.Div(
        children=[
            html.H6("referral.url"),
            dcc.Dropdown(
                id=ids.REFERRAL_DROPDOWN,
                options=unique_referrals,
                value=None,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children="all_referrals",
                id=ids.SELECT_ALL_REFERRALS_BUTTON,
                n_clicks=0,
            ),
        ],
    )
