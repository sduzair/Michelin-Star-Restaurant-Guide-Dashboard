import pandas as pd
from pandas import DataFrame
from pandas._typing import ArrayLike


def standardize_price(price):
    if pd.isna(price):
        return "Unknown"

    return "$" * len(price)


def clean_data(df: DataFrame):
    # Split text using string ',' in column: 'Location'
    loc_0 = df.columns.get_loc("Location")
    df_clean_split = (
        df["Location"].str.split(pat=",", expand=True).add_prefix("Location_")
    )
    df = pd.concat([df.iloc[:, :loc_0], df_clean_split, df.iloc[:, loc_0:]], axis=1)
    # Rename column 'Location_0' to 'Location_city'
    df = df.rename(columns={"Location_0": "Location_city"})
    # Rename column 'Location_1' to 'Location_country'
    df = df.rename(columns={"Location_1": "Location_country"})
    # Fill missing country values with this dict
    city_country_map = {
        "Singapore": "Singapore",
        "Hong Kong": "China",
        "Macau": "China",
        "Dubai": "United Arab Emirates",
        "Luxembourg": "Luxembourg",
        "Abu Dhabi": "United Arab Emirates",
    }
    df["Location_country"] = df["Location_country"].fillna(
        df["Location_city"].map(city_country_map)
    )
    # Created column 'Standardized_Price' from formula
    df["Standardized_Price"] = df["Price"].apply(standardize_price)
    return df


def select_unique_location_city_where_location_country_is_missing(
    df: DataFrame,
) -> ArrayLike:
    # Filter rows based on column: 'Location_country'
    df_temp = df[df["Location_country"].isna()]
    return df_temp["Location_city"].unique()


def get_facilitiesandservices_df(df: DataFrame):
    # Create a new DataFrame with Name, Address, and all facilities and services in one column
    df_facilitiesandservices = df[["Name", "Address", "FacilitiesAndServices"]]
    df_facilitiesandservices["FacilitiesAndServices"] = df_facilitiesandservices[
        "FacilitiesAndServices"
    ].str.split(",")
    df_facilitiesandservices = df_facilitiesandservices.explode("FacilitiesAndServices")
    df_facilitiesandservices["FacilitiesAndServices"] = df_facilitiesandservices[
        "FacilitiesAndServices"
    ].str.strip()
    # Reset the index
    # df_facilitiesandservices = df_facilitiesandservices.reset_index(drop=True)

    return df_facilitiesandservices


def get_cuisine_df(df: DataFrame):
    # Create a new DataFrame with Name, Address, and all cuisines in one column
    df_cuisine = df[["Name", "Address", "Cuisine"]]
    df_cuisine["Cuisine"] = df_cuisine["Cuisine"].str.split(",")
    df_cuisine = df_cuisine.explode("Cuisine")
    df_cuisine["Cuisine"] = df_cuisine["Cuisine"].str.strip()
    # Reset the index
    # df_cuisine = df_cuisine.reset_index(drop=True)

    return df_cuisine


CSV_PATH = "data/michelin_by_Jerry_Ng.csv"


def read_csv(path: str):
    return pd.read_csv("data/michelin_by_Jerry_Ng.csv")
