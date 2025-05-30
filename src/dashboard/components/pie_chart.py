import plotly.express as px

from dash import dcc, html, callback
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids


def render(data: DataFrame) -> html.Div:
    df: DataFrame = data.copy()

    @callback(
        Output(ids.PIE_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CODE_DROPDOWN, "value"),
        ],
    )
    def update_pie_chart(
        years: list[str], months: list[str], codes: list[str]
    ) -> html.Div:
        filtered_data = df.query(
            "YEAR in @years and MONTH in @months and CODE in @codes"
        )
        if filtered_data.shape[0] == 0:
            return html.Div("general.no_data", id=ids.PIE_CHART)
        fig = px.pie(filtered_data, values="CODE", names="MONTH")
        # fig.show()
        # pie = go.Pie(
        #     labels=df["CODE"],
        #     values=df["MONTH"],
        #     hole=0.5,
        # )

        # fig = go.Figure(data=[pie])
        # fig.update_layout(margin={"t": 40, "b": 0, "l": 0, "r": 0})
        # fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")

        return html.Div(dcc.Graph(figure=fig), id=ids.PIE_CHART)

    return html.Div(id=ids.PIE_CHART)
