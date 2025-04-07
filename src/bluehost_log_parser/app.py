import logging
import pandas as pd
import plotly.express as px

from dash import Dash, html, dash_table, dcc
from bluehost_log_parser import my_secrets
from logging import Logger
from sqlalchemy import create_engine, Engine, exc

logger: Logger = logging.getLogger(__name__)


try:
    engine: Engine = create_engine(f"mysql+pymysql://{my_secrets.local_dburi}")

except exc.SQLAlchemyError as e:
    logger.critical(str(e))
    exit()



df = pd.read_sql_table(con=engine.connect(), table_name="logs")
df.where((df["CODE"] == '200') & (df["REF_URL"] == "hoa.tascs.net"), inplace=True)
df.sort_values("ACCESSED", inplace=True, ascending=False)
print(df.info())

app = Dash()

app.layout = [
    html.Div(children='Webserver Logs App'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=25),
    dcc.Graph(figure=px.histogram(df, x='AGENT', y='SIZE', histfunc='avg'))

]
if __name__ == '__main__':
    app.run(debug=True)
