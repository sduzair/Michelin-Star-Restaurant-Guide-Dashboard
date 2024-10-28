from dotenv import load_dotenv
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import numpy as np

from src.data_cleaning import CSV_PATH, clean_data, read_csv
from src.figures import award_by_city_scattermap

load_dotenv()

df_clean = clean_data(read_csv(CSV_PATH))

dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

app.layout = [
    dcc.Dropdown(
        np.sort(df_clean["Location_city"].unique()), "Dubai", id="city_dropdown"
    ),
    dcc.Graph(figure={}, id="award_by_city_scattermap"),
]


@callback(
    Output(component_id="award_by_city_scattermap", component_property="figure"),
    Input(component_id="city_dropdown", component_property="value"),
)
def update_graph(city):
    fig = award_by_city_scattermap(df_clean, city)
    return fig


if __name__ == "__main__":
    app.run()
