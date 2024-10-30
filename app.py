import dash_bootstrap_components as dbc
import numpy as np
from dash import Dash, Input, Output, State, callback, dcc, html
from dotenv import load_dotenv

from src.data_cleaning import CSV_PATH, clean_data, read_csv
from src.figures import award_by_city_scattermap, awards_by_city_bar

load_dotenv()

df_clean = clean_data(read_csv(CSV_PATH))
unique_awards = np.sort(df_clean["Award"].unique())
unique_cities = np.sort(df_clean["Location_city"].unique())


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css])

app.layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        unique_cities,
                        "Paris",
                        placeholder="Select a city",
                        id="city_dropdown",
                    ),
                ),
                dbc.Col(
                    dcc.Dropdown(
                        unique_awards,
                        unique_awards,
                        multi=True,
                        placeholder="Select multiple award recognitions",
                        id="award_multi_dropdown",
                    ),
                ),
            ],
            class_name="g-0",
        ),
        dbc.Row(
            dbc.Col(
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(figure={}, id="award_by_city_scattermap"),
                            class_name="col-md-9",
                        ),
                        dbc.Col(
                            dcc.Graph(figure={}, id="awards_by_city_bar"),
                            class_name="col-md-3",
                        ),
                    ],
                    class_name="g-0",
                ),
            ),
            class_name="g-0",
        ),
    ],
    className="dbc container-fluid gx-0 d-flex flex-column min-vh-100 justify-content-between",
)


@callback(
    Output("award_multi_dropdown", "options"),
    Output("award_multi_dropdown", "value"),
    Input(component_id="city_dropdown", component_property="value"),
)
def update_graph_for_city(city):
    city_data = df_clean[df_clean["Location_city"] == city]
    city_awards = np.sort(city_data["Award"].unique())
    options = [{"label": award, "value": award} for award in city_awards]
    values = city_awards
    return options, values


@callback(
    Output(component_id="award_by_city_scattermap", component_property="figure"),
    Output(component_id="awards_by_city_bar", component_property="figure"),
    Input(component_id="award_multi_dropdown", component_property="value"),
    State(component_id="city_dropdown", component_property="value"),
)
def update_graph_for_award(awards, city):
    fig_1 = award_by_city_scattermap(df_clean, city, awards)
    fig_2 = awards_by_city_bar(df_clean, city, awards)

    return fig_1, fig_2


if __name__ == "__main__":
    app.run()
