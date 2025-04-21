import plotly.express as px

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids


def render(app: Dash, source: DataFrame) -> html.Div:
    @app.callback(
        Output(ids.BAR_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CODE_DROPDOWN, "value"),
        ],
    )
    def update_bar_chart(
        years: list[str], months: list[str], codes: list[str]
    ) -> html.Div:
        fig = px.bar(
            source,
            x=source["CODE"],
            y=source["AGENT"],
            color=source["YEAR"],
            labels={
                "code": "general.month",
                "month": "general.code",
            },
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)
