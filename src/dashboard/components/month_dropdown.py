from dash import dcc, html, callback
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids


def render(source: DataFrame) -> html.Div:
    df: DataFrame = source.copy()
    all_months: list[str] = df["MONTH"].tolist()
    unique_months: list[str] = sorted(set(all_months))

    @callback(
        Output(ids.MONTH_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_MONTHS_BUTTON, "n_clicks"),
        ],
    )
    def select_all_months(years: list[str], _: int) -> list[str]:
        return unique_months

    return html.Div(
        children=[
            html.H6("month"),
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                options=[{"label": month, "value": month} for month in unique_months],
                value=unique_months,
                multi=True,
            ),
            html.Button(
                className="dropdown-button",
                children=["all_months"],
                id=ids.SELECT_ALL_MONTHS_BUTTON,
                n_clicks=0,
            ),
        ]
    )
