import plotly.express as px

from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids


def render(app: Dash, data: DataFrame) -> html.Div:
    df = data.copy()

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
        filtered_data = df.query(
            "YEAR in @years and MONTH in @months and CODE in @codes"
        )

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.BAR_CHART)

        #  ISSUE WITH KEYS month name
        def create_pivot_table() -> DataFrame:
            pt = filtered_data.pivot_table(
                values=filtered_data["MONTH"],
                index=filtered_data["CODE"],
                aggfunc="sum",
                fill_value=0,
                dropna=False,
            )
            return pt.reset_index().sort_values(filtered_data["CODE"], ascending=False)

        fig = px.bar(
            filtered_data,
            # create_pivot_table(),
            x=filtered_data["CODE"],
            y=filtered_data["MONTH"],
            color=filtered_data["YEAR"],
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)
