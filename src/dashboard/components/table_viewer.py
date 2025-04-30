# https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Ag-Grid/introduction/ag-grid-intro2.py
import dash_ag_grid as dag

from pandas import DataFrame
from dash import Dash, html, register_page
from dash.dependencies import Input, Output
from logging import Logger
from . import ids

# register_page(__name__, path="/")


# deleteable=True only on column defining? Can remove rows obly for datatable!
def render(app: Dash, data: DataFrame) -> html.Div:
    df = data.copy()
    df["SIZE"] = df["SIZE"].apply(lambda s: int("0") if not s.isdigit() else int(s))
    del df["REF_IP"]

    columnDefs = []
    for i in df.columns:
        if i == "ACCESSED":
            columnDefs.append({"field": i, "filter": "agDateColumnFilter"})
        elif i == "SIZE" or i == "YEAR":
            columnDefs.append({"field": i, "filter": "agNumberColumnFilter"})

        else:
            columnDefs.append({"field": i})

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
            "paginationAutoPageSize": True,
            "domLayout": "autoHeight",
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
