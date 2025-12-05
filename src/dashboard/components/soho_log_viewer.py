# https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Ag-Grid/introduction/ag-grid-intro2.py
import dash_ag_grid as dag
import logging

from pandas import DataFrame
from dash import html
from logging import Logger
from . import ids

logger: Logger = logging.getLogger(__name__)


def render(data: DataFrame) -> html.Div:
    df: DataFrame = data.copy()
    del df["ACCESSED"]
    del df["SOURCE"]
    columnDefs = []
    for col in df.columns:
        if col == "YEAR" or col == "MONTH" or col == "ALPHA2":
            continue
        if col == "DATE":
            columnDefs.append({"field": col, "filter": "agDateColumnFilter"})
        elif col == "SIZE" or col == "YEAR" or col == "RESPONSE":
            columnDefs.append({"field": col, "filter": "agNumberColumnFilter"})

        else:
            columnDefs.append({"field": col})

    defaultColDef = {
        "resizable": True,
        "editable": True,
        "headerClass": "center-aligned-header",
        "filter": "agTextColumnFilter",
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

    if df.shape[0] == 0:
        return html.Div("general.no_data", id=ids.PIE_CHART)

    logger.info("Log Viewer AG Grid CREATED")

    return html.Div(
        children=[grid],
        className="table",
    )
