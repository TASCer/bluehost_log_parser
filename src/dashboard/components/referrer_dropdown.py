from dash import dcc, html, callback
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids


def render(data: DataFrame) -> html.Div:
    all_referrers: list[str] = data["REFERRER"].tolist()
    unique_referrers: list[str] = sorted(set(all_referrers))
    default_referrer_idx = unique_referrers.index("-")
    default_referrer = unique_referrers[default_referrer_idx]

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
            html.H6("referrer"),
            dcc.Dropdown(
                id=ids.REFERRER_DROPDOWN,
                options=unique_referrers,
                value=default_referrer,
                multi=False,
            ),
            html.Button(
                className="dropdown-button",
                children="all_referrers",
                id=ids.SELECT_ALL_REFERRERS_BUTTON,
                n_clicks=0,
            ),
        ],
    )
