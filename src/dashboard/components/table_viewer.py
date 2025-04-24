from pandas import DataFrame
from dash import dash_table, Dash, html




def render(app: Dash, source: DataFrame) -> html.Div:
    df = source.copy()
    df.sort_values("ACCESSED", ascending=False, inplace=True)
    return dash_table.DataTable(df.to_dict('records'),columns=[
            {"name": i, "id": i, "deletable": True, "selectable": True} for i in df.columns], 
            # id="tbl"),
            # dbc.Alert(id='tbl_out'),
    )    