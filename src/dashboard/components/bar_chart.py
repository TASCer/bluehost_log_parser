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
            data_frame=filtered_data,
            # create_pivot_table(),
            x="CODE",
            y="SOURCE",
            color="MONTH",
        )
        logger.info("PLOT CREATED")
        return html.Div(dcc.Graph(figure=fig), id=ids.BAR_CHART)

    return html.Div(id=ids.BAR_CHART)
