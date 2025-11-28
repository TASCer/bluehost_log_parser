import plotly.express as px
import logging

from dash import dcc, html, callback
from dash.dependencies import Input, Output
from logging import Logger
from pandas import DataFrame
from . import ids

logger: Logger = logging.getLogger(__name__)


def render(data: DataFrame) -> html.Div:
    df: DataFrame = data.copy()

    @callback(
        Output(ids.PIE_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.RESPONSE_DROPDOWN, "value"),
            Input(ids.REFERRER_DROPDOWN, "value"),
        ],
    )
    def update_pie_chart(
        years: list[str], months: list[str], responses: list[str], referrers: list[str]
    ) -> html.Div:
        filtered_data: DataFrame = df.query(
            "YEAR in @years and MONTH in @months and RESPONSE in @responses and REFERRER in @referrers"
        )
        if filtered_data.shape[0] == 0:
            return html.Div("general.no_data", id=ids.PIE_CHART)
        fig = px.pie(filtered_data, values="RESPONSE", names="SITE")
        fig.update_traces(textinfo="label")

        logger.info("PIE CHART CREATED")

        return html.Div(dcc.Graph(figure=fig), id=ids.PIE_CHART)

    return html.Div(id=ids.PIE_CHART)
