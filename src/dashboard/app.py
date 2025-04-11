# https://github.com/ArjanCodes/2022-dash
import logging
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import Dash, dash_table  # , dcc
from logging import Logger
from dashboard.data import loader

# from dash.dependencies import Input, Output
from dashboard.components import layout

logger: Logger = logging.getLogger(__name__)


def main():
    df = loader.load_weblog_data()
    # df.where((df["CODE"] == "200") & (df["REF_URL"] == "cpanel.cag.bis.mybluehost.me"), inplace=True)
    # df.sort_values("ACCESSED", inplace=True, ascending=False)
    df_group = df.groupby(by="REF_URL")
    refs = [r for r in df_group.groups]
    print("REF", refs, len(refs))

    app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = layout.create_layout(app)
    app.layout = [
        dbc.Alert("Webserver Logs App", className="m-5"),
        dash_table.DataTable(data=df.to_dict("records"), page_size=25),
        # dcc.Graph(figure=px.histogram(df, x="AGENT", y="SIZE", histfunc="avg")),
    ]

    app.run(debug=True)


if __name__ == "__main__":
    main()
