from dash import Dash, dcc, html, callback
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids
# from .dropdown_helper import to_dropdown_options


def render(source: DataFrame) -> html.Div:
    df: DataFrame = source.copy()
    all_years: list[str] = df["YEAR"]
    unique_years: list[str] = sorted(set(all_years), key=int)

    @callback(
        Output(ids.YEAR_DROPDOWN, "value"),
        Input(ids.SELECT_ALL_YEARS_BUTTON, "n_clicks"),
    )
    def select_all_years(_: int) -> list[str]:
        return unique_years

    return html.Div(
        children=[
            html.H6("year"),
            dcc.Dropdown(
                id=ids.YEAR_DROPDOWN,
                options=[{"label": year, "value": year} for year in unique_years],
                value=unique_years,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=["all_years"],
                id=ids.SELECT_ALL_YEARS_BUTTON,
                n_clicks=0,
            ),
        ]
    )
