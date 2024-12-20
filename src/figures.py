from typing import List

import plotly.express as px
import plotly.graph_objects as go
from pandas import DataFrame
from plotly.graph_objs._figure import Figure

from src.facility_award_correlation import (
    award_ranking,
    calculate_award_facility_correlations,
)

color_map = {
    "3 Stars": "#FFD700",  # Gold
    "2 Stars": "#C0C0C0",  # Silver
    "1 Star": "#CD7F32",  # Bronze
    "Bib Gourmand": "#4CAF50",  # Green
    "Selected Restaurants": "#2196F3",  # Blue
}


def awards_by_city_bar(df: DataFrame, city: str, awards: List[str] = []):
    # Filter the dataframe for the specified city
    df_city = df[df["Location_city"] == city]

    # Apply awards filter only if the awards list is not empty
    if awards:
        df_city = df_city[df_city["Award"].isin(awards)]

    # Group by Award and count the occurrences
    df_grouped = df_city.groupby("Award").size().reset_index(name="Count")

    # Map the custom ranking to the 'Award' column
    df_grouped["Rank"] = df_grouped["Award"].map(award_ranking)

    # Sort the dataframe by Rank in descending order
    df_grouped = df_grouped.sort_values("Rank", ascending=True)

    fig = px.bar(
        df_grouped,
        x="Award",
        y="Count",
        color="Award",
        color_discrete_map=color_map,
        labels={"Award": "Michelin Recognition", "Count": "Number of Restaurants"},
    )

    # Update the layout to position the legend
    fig.update_layout(
        legend=dict(yanchor="top", y=0.98, xanchor="right", x=0.99),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    return fig


def award_by_city_scattermap(df: DataFrame, city: str, awards: List[str] = []):
    # Filter the dataframe for the specified city
    city_data = df[df["Location_city"] == city]

    # Apply awards filter only if the awards list is not empty
    if awards:
        city_data = city_data[city_data["Award"].isin(awards)]
    # country = city_data["Location_country"].iloc[0]

    fig = px.scatter_map(
        data_frame=city_data,
        lat="Latitude",
        lon="Longitude",
        color="Award",
        color_discrete_map=color_map,
        hover_data={
            "Latitude": False,
            "Longitude": False,
            "Address": True,
            "Url": True,
            "PhoneNumber": True,
            "GreenStar": True,
        },
        zoom=10,
        map_style="carto-voyager",  # Light map style
    )
    # Update the layout to position the legend
    fig.update_layout(
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.01),
        legend_title_text="Michelin Guide Awards",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    return fig


def get_top_cuisines(df: DataFrame) -> DataFrame:
    # Step 1: Group by city and facilities/services, then count
    grouped = df.groupby(["Location_city", "Cuisine"]).size().reset_index(name="count")

    # Step 2: Sort the values within each city group by count in descending order
    sorted_grouped = grouped.sort_values(
        ["Location_city", "count"], ascending=[True, False]
    )

    # # Step 3: Select the top 5 facilities/services for each city
    # top_5 = sorted_grouped.groupby("Location_city").head(5)

    # Step 4: Reset the index for cleaner output
    result = sorted_grouped.reset_index(drop=True)
    return result


def create_correlation_heatmap(
    df_encoded: DataFrame, city_name: str, theme: str
) -> Figure:
    correlation_df = calculate_award_facility_correlations(df_encoded, city_name)

    # Remove NA rows
    correlation_df = correlation_df.dropna()

    # Prepare data for heatmap
    facilities = correlation_df.index
    correlations = correlation_df["correlation"]
    # p_values = correlation_df["p_value"]

    # Choose colorscale based on theme
    if theme == "dark":
        colorscale = "Viridis"  # A good choice for dark themes
    else:
        colorscale = "RdBu_r"  # Original colorscale for light themes

    # Create heatmap
    fig = go.Figure(
        data=go.Heatmap(
            z=[correlations],
            x=[
                facility.replace("FacilitiesAndServices_", "")
                for facility in facilities
            ],
            colorscale=colorscale,
            zmin=-1,
            zmax=1,
        )
    )

    # Update layout
    fig.update_layout(
        title=f"Correlation between Facilities/Services and Michelin Award in {city_name}",
        xaxis_title="Facilities and Services",
        yaxis_title="Michelin Award Correlation",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False, visible=True),
    )

    return fig
