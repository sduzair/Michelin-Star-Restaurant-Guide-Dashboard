from typing import List
import plotly.express as px
from pandas import DataFrame

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
    # Sort the dataframe by Count in descending order
    df_grouped = df_grouped.sort_values("Count", ascending=False)
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
    )
    # Update the layout to position the legend
    fig.update_layout(
        legend=dict(yanchor="top", y=0.98, xanchor="left", x=0.01),
        legend_title_text="Michelin Guide Awards",
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )

    return fig
