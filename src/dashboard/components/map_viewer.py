import plotly.express as px

from dash import dcc, html, callback
from dash.dependencies import Input, Output
from pandas import DataFrame
from . import ids


def render(data: DataFrame) -> html.Div:
    df: DataFrame = data.copy()

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
    # fig = px.scatter_geo(
    #     df,
    #     locations="iso_alpha",
    #     color="continent",
    #     hover_name="country",
    #     size="pop",
    #     projection="natural earth",
    # )
    # fig.show()

    # return html.Div(id=ids.PIE_CHART)
