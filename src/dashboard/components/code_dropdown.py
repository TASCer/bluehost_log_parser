import i18n
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from ..data.source import DataSource
from . import ids
from .dropdown_helper import to_dropdown_options


def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.CODE_DROPDOWN, "value"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_CODES_BUTTON, "n_clicks"),
        ],
    )
    def select_all_categories(years: list[str], months: list[str], _: int) -> list[str]:
        return source.filter(years=years, months=months).unique_codes

    return html.Div(
        children=[
            html.H6(i18n.t("general.code")),
            dcc.Dropdown(
                id=ids.CODE_DROPDOWN,
                options=to_dropdown_options(source.unique_codes),
                value=source.unique_codes,
                multi=True,
                placeholder=i18n.t("general.select"),
            ),
            html.Button(
                className="dropdown-button",
                children=[i18n.t("general.select_all")],
                id=ids.SELECT_ALL_CODES_BUTTON,
                n_clicks=0,
            ),
        ],
    )
