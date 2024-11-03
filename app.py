import dash_bootstrap_components as dbc
import numpy as np
from dash import (
    Dash,
    Input,
    Output,
    State,
    callback,
    dash_table,
    dcc,
    html,
    clientside_callback,
)
from dotenv import load_dotenv

from src.data_cleaning import CSV_PATH, clean_data, get_exploded_cuisine_df, read_csv
from src.facility_award_correlation import clean_and_encode_facilities, encode_award
from src.figures import (
    award_by_city_scattermap,
    awards_by_city_bar,
    create_correlation_heatmap,
    get_top_cuisines,
)

load_dotenv()

df_clean = clean_data(read_csv(CSV_PATH))
unique_awards = np.sort(df_clean["Award"].unique())
unique_cities = np.sort(df_clean["Location_city"].unique())


fa_css = (
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css"
)
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc_css, fa_css])

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
                    class_name="col-3",
                ),
                dbc.Col(
                    dcc.Dropdown(
                        unique_awards,
                        unique_awards,
                        multi=True,
                        placeholder="Select multiple award recognitions",
                        id="award_multi_dropdown",
                    ),
                    class_name="col-6",
                ),
                html.Div(
                    [
                        html.Span(
                            [
                                dbc.Label(className="fas fa-sun", html_for="switch"),
                                dbc.Switch(
                                    id="switch",
                                    value=False,
                                    className="d-inline-block ms-1",
                                    persistence=True,  # Enable persistence
                                    persistence_type="local",  # Store in local storage
                                ),
                                dbc.Label(className="fas fa-moon", html_for="switch"),
                            ]
                        ),
                        dcc.Store(id="theme-store", storage_type="local"),
                    ],
                    className="col-3 d-flex justify-content-end align-self-center",
                ),
            ],
            class_name="g-0 row-cols-auto",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Graph(figure={}, id="facility_award_correlation_heatmap"),
                    class_name="col-md-9",
                ),
                dbc.Col(
                    dash_table.DataTable(
                        page_size=5,
                        style_table={"height": "200px", "overflowY": "auto"},
                        style_cell_conditional=[
                            {"if": {"column_id": "Cuisine"}, "textAlign": "left"},
                            {"if": {"column_id": "Count"}, "width": "100px"},
                        ],
                        sort_action="native",
                        id="top_5_cuisines_table",
                    ),
                    class_name="col-md-3",
                ),
            ],
            class_name="g-0",
        ),
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
    ],
    className="dbc container-fluid gx-0 d-flex flex-column min-vh-100 justify-content-between",
)


@callback(
    Output("award_multi_dropdown", "options"),
    Output("award_multi_dropdown", "value"),
    Input(component_id="city_dropdown", component_property="value"),
)
def update_multi_dropdown(by_city):
    city_data = df_clean[df_clean["Location_city"] == by_city]
    city_awards = np.sort(city_data["Award"].unique())
    options = [{"label": award, "value": award} for award in city_awards]
    values = city_awards
    return options, values


@callback(
    Output(component_id="award_by_city_scattermap", component_property="figure"),
    Output(component_id="awards_by_city_bar", component_property="figure"),
    Input("theme-store", "data"),
    Input(component_id="award_multi_dropdown", component_property="value"),
    State(component_id="city_dropdown", component_property="value"),
)
def update_scattermap_and_city_bar(theme: str, by_awards, by_city):
    fig_1 = award_by_city_scattermap(df_clean, by_city, by_awards)
    fig_2 = awards_by_city_bar(df_clean, by_city, by_awards)

    # Update the template based on the theme
    template = "plotly_dark" if theme == "dark" else "plotly"

    # Update scatter map
    if theme == "dark":
        fig_1.update_layout(
            template=template,
            map_style="carto-darkmatter",  # Dark map style
        )
    else:
        fig_1.update_layout(
            template=template,
            map_style="carto-voyager",  # Light map style
        )

    # Update bar chart
    fig_2.update_layout(template=template)

    return fig_1, fig_2


df_top_cuisines = get_top_cuisines(get_exploded_cuisine_df(df_clean))


@callback(
    Output(component_id="top_5_cuisines_table", component_property="data"),
    Output(component_id="top_5_cuisines_table", component_property="columns"),
    Input(component_id="city_dropdown", component_property="value"),
)
def update_top_cuisines_table(by_city: str):
    df_top_for_city = df_top_cuisines[df_top_cuisines["Location_city"] == by_city][
        ["Cuisine", "count"]
    ]
    # Convert column names to PascalCase
    df_top_for_city.columns = df_top_for_city.columns.str.title()
    return (
        df_top_for_city.to_dict("records"),
        [{"name": i, "id": i} for i in df_top_for_city.columns],
    )


df_encoded_awards_and_fns = clean_and_encode_facilities(encode_award(df_clean.copy()))


@callback(
    Output(
        component_id="facility_award_correlation_heatmap", component_property="figure"
    ),
    Input("theme-store", "data"),
    Input(component_id="city_dropdown", component_property="value"),
)
def update_facility_award_correlation_heatmap(theme: str, by_city: str):
    fig = create_correlation_heatmap(df_encoded_awards_and_fns, by_city, theme)

    # Update the template based on the theme
    template = "plotly_dark" if theme == "dark" else "plotly"
    fig.update_layout(template=template)

    return fig


clientside_callback(
    """
    function(switchOn) {
        const theme = switchOn ? 'dark' : 'light';
        document.documentElement.setAttribute('data-bs-theme', theme);
        
        // Set background color based on switch state
        document.body.style.backgroundColor = switchOn ? '#111111' : '#FFFFFF';  // Dark or light background
        
        return theme;
    }
    """,
    Output("theme-store", "data"),
    Input("switch", "value"),
)


if __name__ == "__main__":
    app.run()
