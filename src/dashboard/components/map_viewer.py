import plotly.express as px
import logging

from dash import dcc, html, callback
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids
from bluehost_log_parser import update_sources
from logging import Logger


logger: Logger = logging.getLogger(__name__)


def render(data: DataFrame) -> html.Div:
    """
    Function finds and adds asn_alpha 3-letter country code to the provided df.

    """
    df: DataFrame = data.copy()
    # TODO rework, too slow
    asn_alphas: list[str] = update_sources.asn_alphas(df["ALPHA2"])
    df["ALPHA"] = asn_alphas
    df = df[["ALPHA", "ACCESSED", "COUNTRY"]]

    group_countries: DataFrame = df.groupby(
        ["COUNTRY", "ALPHA"], as_index=False
    ).count()

    group_countries = group_countries.sort_values(by="ACCESSED", ascending=False)
    top_countries = group_countries[:11].reset_index(drop=True)

    fig = px.scatter_geo(
        top_countries,
        locations="ALPHA",
        color="COUNTRY",
        hover_name="ALPHA",
        size="ACCESSED",
        projection="natural earth",
        width=1600,
        height=800,
        title="SOURCE ACTIVITY LOCATIONS",
        fitbounds="locations",
        # animation_frame="ACCESSED", # need to rework df to get this to work ()
    )
    logger.info("GEO SCATTER MAP CREATED")

    return html.Div(dcc.Graph(figure=fig), id=ids.MAP_VIEWER)


# @callback(
#     Output(ids.PIE_CHART, "children"),
#     [
#         Input(ids.YEAR_DROPDOWN, "value"),
#         Input(ids.MONTH_DROPDOWN, "value"),
#         Input(ids.CODE_DROPDOWN, "value"),
#         Input(ids.REFERRAL_DROPDOWN, "value"),
#     ],
# )
# def update_pie_chart(
#     years: list[str], months: list[str], codes: list[str], referrals: list[str]
# ) -> html.Div:
#     filtered_data: DataFrame = df.query(
#         "YEAR in @years and MONTH in @months and CODE in @codes and REF_URL in @referrals"
#     )
#     if filtered_data.shape[0] == 0:
#         return html.Div("general.no_data", id=ids.PIE_CHART)
#     fig = px.pie(filtered_data, values="CODE", names="REF_URL")
#     fig.update_traces(textinfo="label")

#     return html.Div(dcc.Graph(figure=fig), id=ids.PIE_CHART)
