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
    logger.info(f"{len(df)=}")

    @callback(
        Output(ids.BAR_CHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CODE_DROPDOWN, "value"),
            Input(ids.REFERRAL_DROPDOWN, "value"),
        ],
    )
    def update_bar_chart(
        years: list[str], months: list[str], codes: list[str], referrals: list[str]
    ) -> html.Div:
        logger.debug(
            f"YEARS: {years} MONTHS:{months} CODES:{codes} REFERRALS:{referrals}"
        )

        filtered_data = df.query(
            "YEAR in @years and MONTH in @months and CODE in @codes and REF_URL in @referrals"
        )

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected.", id=ids.BAR_CHART)

        fig = px.histogram(
            filtered_data,
            x="CODE",
            color="REF_URL",
        )
        logger.info("BAR CHART CREATED")

        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)
