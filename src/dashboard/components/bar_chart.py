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
        filtered_source = source.filter(years, months, codes)
        if not filtered_source.row_count:
            return html.Div("general.no_data", id=ids.BAR_CHART)

        fig = px.bar(
            filtered_source.create_pivot_table(),
            x=source["MONTH"],
            y=source["CODE"],
            color="CODE",
            labels={
                "code": "general.code",
                "month": "general.month",
            },
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)
