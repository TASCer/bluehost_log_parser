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
        filtered_data = source.query(
            "YEAR in @years and MONTH in @months and CODE in @codes"
        )

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.BAR_CHART)

        # ISSSUE
        def create_pivot_table() -> DataFrame:
            pt = filtered_data.pivot_table(
                values=source["MONTH"],
                index=source["CODE"],
                aggfunc="sum",
                fill_value=0,
                dropna=False,
            )
            return pt.reset_index().sort_values(source["CODE"], ascending=False)

        fig = px.bar(
            # create_pivot_table(),
            x=source["CODE"],
            y=source["MONTH"],
            color=source["CODE"],
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)