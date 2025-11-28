# TODO IMPLEMENT THE dropdown helper?
from dash import dcc, html, callback
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids


def render(source: DataFrame) -> html.Div:
    all_sites: list[str] = source["SITE"].tolist()
    unique_sites: list[str] = sorted(set(all_sites))

    @callback(
        Output(ids.SITE_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_SITES_BUTTON, "n_clicks"),
        ],
    )
    def select_all_sites(years: list[str], months: list[str], _: int) -> list[str]:
        return unique_sites

    return html.Div(
        children=[
            html.H6("site"),
            dcc.Dropdown(
                id=ids.SITE_DROPDOWN,
                options=unique_sites,
                value=unique_sites,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children="all_sites",
                id=ids.SELECT_ALL_SITES_BUTTON,
                n_clicks=0,
            ),
        ],
    )
