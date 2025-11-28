# https://github.com/Coding-with-Adam/Dash-by-Plotly/blob/master/Ag-Grid/introduction/ag-grid-intro2.py
import dash_ag_grid as dag
import logging

from pandas import DataFrame
from dash import html
from dash.dependencies import Input, Output
from logging import Logger
from . import ids

logger: Logger = logging.getLogger(__name__)


def render(data: DataFrame) -> html.Div:
    df: DataFrame = data.copy()
    del df["ACCESSED"]

    columnDefs = []
    for i in df.columns:
        if i == "YEAR" or i == "MONTH" or i == "ALPHA2":
            continue
        if i == "DATE":
            columnDefs.append({"field": i, "filter": "agDateColumnFilter"})
        elif i == "SIZE" or i == "YEAR":
            columnDefs.append({"field": i, "filter": "agNumberColumnFilter"})

        else:
            columnDefs.append({"field": i})

    defaultColDef = {
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

    logger.info("Log AG Grid CREATED")

    return html.Div(
        children=[grid],
        className="table",
    )
