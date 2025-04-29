# TODO GET TABLE VIEW INTERACTIVE w/dag
from pandas import DataFrame
from dash import dash_table, Dash, html
from dash.dependencies import Input, Output
from logging import Logger
from . import ids

import dash_ag_grid as dag 

# deleteable=True only on column defining? Can remove rows!
def render(app: Dash, data: DataFrame) -> html.Div:
    df = data.copy()

    # @app.callback(
    #     Output(ids.PIE_CHART, "children"),
    #     [
    #         Input(ids.YEAR_DROPDOWN, "value"),
    #         Input(ids.MONTH_DROPDOWN, "value"),
    #         Input(ids.CODE_DROPDOWN, "value"),
    #     ],
    # )
    # def update_pie_chart(
    #     years: list[str], months: list[str], codes: list[str]
    # ) -> html.Div:
    # filtered_data = df.query(
    #         "YEAR in @years and MONTH in @months and CODE in @codes"
    #     )
    if df.shape[0] == 0:
        return html.Div("general.no_data", id=ids.PIE_CHART)
    

    return dash_table.DataTable(df.to_dict('records'),columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True, "editable":True} for i in df.columns])
   