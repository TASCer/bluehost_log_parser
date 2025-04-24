# https://dash.plotly.com/datatable
from pandas import DataFrame
from dash import dash_table, Dash, html

import dash_ag_grid as dag


# deleteable=True only on column defining? Can remove rows!
def render(app: Dash, source: DataFrame) -> html.Div:
    data = source.to_dict("records")
    filter_action = ["native"]
    # df.sort_values("ACCESSED", ascending=False, inplace=True)
    return dash_table.DataTable(data, editable=True, column_selectable="multi", cell_selectable=True, row_deletable=True, id="tbl")