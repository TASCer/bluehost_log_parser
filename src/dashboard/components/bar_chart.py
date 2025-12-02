import logging
import plotly.express as px

from dash import dcc, html, callback
from dash.dependencies import Input, Output
from logging import Logger
from pandas import DataFrame
from . import ids

logger: Logger = logging.getLogger(__name__)


def render(data: DataFrame) -> html.Div:
    df: DataFrame = data.copy()
    logger.info("CREATING BAR CHART")

    @callback(
        Output(ids.BAR_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.RESPONSE_DROPDOWN, "value"),
            Input(ids.REFERRER_DROPDOWN, "value"),
            Input(ids.SITE_DROPDOWN, "value"),
        ],
    )
    def update_bar_chart(
        years: list[str],
        months: list[str],
        responses: list[str],
        referrers: list[str],
        sites: list[str],
    ) -> html.Div:

        filtered_data = df.query(
            "YEAR in @years and MONTH in @months and RESPONSE in @responses and REFERRER in @referrers and SITE in @sites"
        )

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.BAR_CHART)

        fig = px.histogram(
            filtered_data,
            x="RESPONSE",
            color="REFERRER",
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)
