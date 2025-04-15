from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dashboard.data.loader import load_weblog_data

# from ..data.source import DataSource
from . import ids
from .dropdown_helper import to_dropdown_options


def render(app: Dash) -> html.Div:
    source = load_weblog_data()
    print()

    @app.callback(
        Output(ids.CATEGORY_DROPDOWN, "value"),
        [
            # Input(ids.YEAR_DROPDOWN, "value"),
            # Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.SELECT_ALL_CATEGORIES_BUTTON, "n_clicks"),
        ],
    )
    def select_all_categories(_: int) -> list[str]:
        return source["CODE"].unique()

    return html.Div(
        children=[
            dcc.Dropdown(
                id=ids.CATEGORY_DROPDOWN,
                options=to_dropdown_options(source["CODE"].unique()),
                value=source["CODE"].unique(),
                multi=True,
                placeholder="general.select",
            ),
            html.Button(
                className="dropdown-button",
                children=["general.select_all"],
                id=ids.SELECT_ALL_CATEGORIES_BUTTON,
                n_clicks=0,
            ),
        ],
    )
