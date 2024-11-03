import pandas as pd
from scipy.stats import pointbiserialr
from sklearn.preprocessing import MultiLabelBinarizer


def clean_and_encode_facilities(df: pd.DataFrame) -> pd.DataFrame:
    # Fill NaN values with empty string
    df["FacilitiesAndServices"] = df["FacilitiesAndServices"].fillna("")

    # Split and clean the facilities
    facilities_list = (
        df["FacilitiesAndServices"]
        .str.split(",")
        .apply(lambda x: [item.strip() for item in x if item.strip()])
    )

    # Use MultiLabelBinarizer for one-hot encoding
    mlb = MultiLabelBinarizer(sparse_output=True)
    facilities_encoded = mlb.fit_transform(facilities_list)

    # Create a DataFrame with the encoded facilities
    facilities_df = pd.DataFrame.sparse.from_spmatrix(
        facilities_encoded,
        columns=[f"FacilitiesAndServices_{f}" for f in mlb.classes_],
        index=df.index,
    )

    # Concatenate the original DataFrame with the encoded facilities
    result_df = pd.concat([df, facilities_df], axis=1)

    return result_df


def encode_award(df: pd.DataFrame):
    award_order = {
        "Selected Restaurants": 1,
        "Bib Gourmand": 2,
        "1 Star": 3,
        "2 Stars": 4,
        "3 Stars": 5,
    }
    df["Award_encoded"] = df["Award"].map(award_order)
    return df


def calculate_award_facility_correlations(df_encoded: pd.DataFrame, city: str):
    # Filter by city
    df_encoded_for_city = df_encoded[df_encoded["Location_city"] == city]
    # Get the list of encoded facility/service columns
    facility_columns = [
        col
        for col in df_encoded_for_city.columns
        if col.startswith("FacilitiesAndServices_")
    ]

    # Calculate point-biserial correlation for each facility/service
    correlations = {}
    for facility in facility_columns:
        # Calculate point-biserial correlation directly
        correlation, p_value = pointbiserialr(
            df_encoded_for_city[facility], df_encoded_for_city["Award_encoded"]
        )

        correlations[facility] = {"correlation": correlation, "p_value": p_value}

    # Convert results to a DataFrame for easier viewing
    results_df = pd.DataFrame.from_dict(correlations, orient="index")
    results_df = results_df.sort_values("correlation", ascending=False)
    return results_df
