from pandas import DataFrame
from dash import Dash, html
from dash.dependencies import Input, Output
from logging import Logger
from . import ids

import dash_ag_grid as dag


# deleteable=True only on column defining? Can remove rows!
def render(app: Dash, data: DataFrame) -> html.Div:
    df = data.copy()
    df["SIZE"] = df["SIZE"].apply(lambda s: int("0") if not s.isdigit() else int(s))
    del df["REF_IP"]
    # print(df.head(5))
    # print(df.info())
    columnDefs = [{"field": i} for i in df.columns]
    print(columnDefs)
    defaultColDef = {
        "editable": True,
        "headerClass": "center-aligned-header",
        "filter": "agTextColumnFilter",
        "deletable": True,
        "floatingFilter": False,
    }

    grid = dag.AgGrid(
        className="ag-theme-balham",
        id="log-grid",
        rowData=df.to_dict("records"),
        defaultColDef=defaultColDef,
        columnSize="responsiveSizeToFit",
        dashGridOptions={
            "rowSelection": "multiple",
            "suppressRowClickSelection": False,
            "animateRows": True,
            "pagination": True,
            "autoHeaderHeight": True,
            "autoHeight": True,
        },
        selectAll=True,
        columnDefs=columnDefs,
    )

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

    return html.Div(
        children=[grid],
        className="table",
    )


# WORKS IN Pycharm
# df["SIZE"] = df["SIZE"].apply(lambda s: int("0") if not s.isdigit() else int(s))
# del df["REF_IP"]
# print(df.head(5))
# print(df.info())

# df_referal_groups = df.groupby(["REF_URL"])

# app = Dash(__name__)

# columnDefs = [{"field": i} for i in df.columns]
# print(columnDefs)
# defaultColDef = {'editable': True, "headerClass": 'center-aligned-header', "filter": "agTextColumnFilter", "deletable": True, "floatingFilter": False}

# grid = dag.AgGrid(
#     className="ag-theme-balham",
#     id="log-grid",
#     rowData=df.to_dict('records'),
#     defaultColDef=defaultColDef,
#     columnSize="responsiveSizeToFit",
#     dashGridOptions={
#         "rowSelection": "multiple",
#         "suppressRowClickSelection": False,
#         "animateRows": True,
#         "pagination": True,
#         "autoHeaderHeight": True,
#         "autoHeight": True
#     },
#     selectAll=True,
#     columnDefs=columnDefs,
# )
# graph = dcc.Graph(id="log-graph")

# app.layout = html.Div([grid, graph])


# @app.callback(
#     Output("log-graph", "figure"),
#     Input("log-grid", "rowData")
# )
# def update_graph(row_data):
#     if row_data is not None:
#         df = pd.DataFrame(row_data)
#         fig = px.bar(df, x="CLIENT", y="ACCESSED", title="File Size By Referrer", color="ACTION")
#         return fig
