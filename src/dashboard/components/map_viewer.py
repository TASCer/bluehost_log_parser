import plotly.express as px
import logging

from dash import dcc, html
from pandas import DataFrame
from . import ids
from logging import Logger


logger: Logger = logging.getLogger(__name__)


def render(data: DataFrame) -> html.Div:
    """
    Function renders a map of countries accessing websites.

    :param data: Dataframe
    :return: html div
    """
    df: DataFrame = data.copy()

    group_countries: DataFrame = df.groupby(
        ["COUNTRY", "ALPHA3"], as_index=False
    ).count()

    group_countries = group_countries.sort_values(by="ACCESSED", ascending=False)
    top_countries: DataFrame = group_countries[:16].reset_index(drop=True)

    fig = px.scatter_geo(
        top_countries,
        locations="ALPHA3",
        color="COUNTRY",
        hover_name="ALPHA3",
        size="ACCESSED",
        projection="natural earth",
        width=1600,
        height=800,
        title="TOP 15 SOURCE LOCATIONS",
        fitbounds="locations",
    )
    logger.info("GEO SCATTER MAP CREATED")

    return html.Div(dcc.Graph(figure=fig), id=ids.MAP_VIEWER)
