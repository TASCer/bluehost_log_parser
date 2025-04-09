# https://github.com/ArjanCodes/2022-dash
import logging
import pandas as pd
import plotly.express as px
from dash_bootstrap_components.themes import BOOTSTRAP
from dash import Dash, html, dash_table, dcc
from bluehost_log_parser import my_secrets
from logging import Logger
from sqlalchemy import create_engine, Engine, exc
from dash.dependencies import Input, Output
# from bluehost_log_parser.components.layout import create_layout

logger: Logger = logging.getLogger(__name__)


def main():
        

    try:
        engine: Engine = create_engine(f"mysql+pymysql://{my_secrets.local_dburi}")

    except exc.SQLAlchemyError as e:
        logger.critical(str(e))
        exit()


    df = pd.read_sql_table(con=engine.connect(), table_name="logs")
    df.where((df["CODE"] == "200") & (df["REF_URL"] == "tascs.net:443"), inplace=True)
    df.sort_values("ACCESSED", inplace=True, ascending=False)
    df_group = df.groupby(by="REF_URL")
    refs = [r for r in df_group.groups]
    print(refs)

    app = Dash()
    # app.layout = create_layout(app, df)
    app.layout = [
        html.Div(children="Webserver Logs App"),
        dash_table.DataTable(data=df.to_dict("records"), page_size=25),
        dcc.Graph(figure=px.histogram(df, x="AGENT", y="SIZE", histfunc="avg")),
    ]

    app.run(debug=True)


if __name__ == "__main__":
    main()    