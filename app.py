import dash_bootstrap_components as dbc
import numpy as np
from dash import Dash, Input, Output, State, callback, dcc, html, dash_table
from dotenv import load_dotenv

from src.facility_award_correlation import clean_and_encode_facilities, encode_award
from src.data_cleaning import CSV_PATH, clean_data, get_exploded_cuisine_df, read_csv
from src.figures import (
    award_by_city_scattermap,
    awards_by_city_bar,
    create_correlation_heatmap,
    get_top_5_cuisines,
)

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
            [
                dbc.Col(
                    dcc.Graph(figure={}, id="facility_award_correlation_heatmap"),
                    class_name="col-md-9",
                ),
                dbc.Col(
                    dash_table.DataTable(
                        id="top_5_cuisines_table",
                    ),
                    class_name="col-md-3",
                ),
            ]
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


df_top_5_cuisines = get_top_5_cuisines(get_exploded_cuisine_df(df_clean))


@callback(
    Output(component_id="top_5_cuisines_table", component_property="data"),
    Output(component_id="top_5_cuisines_table", component_property="columns"),
    Input(component_id="city_dropdown", component_property="value"),
)
def update_top_5_cuisines_table(city: str):
    df_top_5_for_city = df_top_5_cuisines[df_top_5_cuisines["Location_city"] == city]
    return (
        df_top_5_for_city.to_dict("records"),
        [{"name": i, "id": i} for i in df_top_5_for_city.columns],
    )


df_encoded_awards_and_fns = clean_and_encode_facilities(encode_award(df_clean.copy()))


@callback(
    Output(
        component_id="facility_award_correlation_heatmap", component_property="figure"
    ),
    Input(component_id="city_dropdown", component_property="value"),
)
def update_facility_award_correlation_heatmap(city_name: str):
    fig = create_correlation_heatmap(df_encoded_awards_and_fns, city_name)
    return fig


if __name__ == "__main__":
    app.run()
