import io
import re
import pandas as pd

from utils.utils_gcp_storage import (
    download_blob_into_memory,
    list_blobs_with_prefix,
)


from utils.libs import save_file
from utils.variables import lst_formats_accepted

lst_formats_accepted = ["7", "10", "12", "LP", "TEST PRESS"]

from airflow.models import Variable


def update_format(df: pd.DataFrame) -> pd.DataFrame:
    """
    Update the vinyl_format column in the DataFrame to uppercase.

    Args:
        df (pd.DataFrame): The DataFrame containing the vinyl data.

    Returns:
        pd.DataFrame: The updated DataFrame with vinyl_format in uppercase.
    """

    # remove spaces and special characters
    df["vinyl_format"] = (
        df["vinyl_format"].astype(str).str.replace(r"[\s\W]+", " ", regex=True)
    )

    dict_replace = {
        "2XLP": "LP",
        "3XLP": "LP",
        "LP 12": "LP",
        "7 CD": "7",
        "12X2": "12",
    }

    # remove vinyl with format CD
    df = df[df["vinyl_format"] != "CD"]

    # Upper vinyl_format
    df["vinyl_format"] = df["vinyl_format"].str.upper()

    # replace formats
    df["vinyl_format"] = df["vinyl_format"].replace(dict_replace)

    # control accepted formats
    lst_formats = [value for value in df["vinyl_format"].unique()]
    for value in lst_formats:
        if value not in lst_formats_accepted:
            raise ValueError(
                f"vinyl_format '{value}' is not in the accepted formats: {lst_formats_accepted}"
            )

    return df


def update_price_currency(df: pd.DataFrame) -> pd.DataFrame:
    """
    Update the vinyl_price and vinyl_currency columns in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing the vinyl data.

    Returns:
        df (pd.DataFrame): The updated DataFrame with vinyl_price and vinyl_currency formatted.
    """

    # replace , with . for regex
    df["vinyl_price"] = df["vinyl_price"].replace(",", ".", regex=True)

    # keep only special characters
    df["vinyl_currency"] = (
        df["vinyl_price"]
        .astype(str)
        .str.replace(r"[\d.,\s]+|\(TTC\)", "", regex=True)
        .str.strip()
    )

    # remove Epuisé
    df = df[~df["vinyl_price"].str.contains("Epuisé", na=False)]

    # split vinyl_price
    # Convert vinyl_price to string and remove non-numeric characters
    df["vinyl_price"] = (
        df["vinyl_price"].astype(str).str.replace(r"[^\d.]", "", regex=True)
    )

    # Convert to float filling NaN with 0
    df.loc[:, "vinyl_price"] = pd.to_numeric(df["vinyl_price"], errors="coerce")
    df.loc[:, "vinyl_price"] = df["vinyl_price"].fillna(0)

    return df


def transform_data(bucket_name: str, time_file_name: str):
    """
    Transform data from a all shops present in folder extract_{time_file_name} in GCP Storage.

    Args:
        bucket_name (str): The name of the GCP Storage bucket to upload the transformed data.
        time_file_name (str): The timestamp used for naming the file.
    """

    df = pd.DataFrame()

    # # Get the list of files with prefix
    # prefix = f"extract_{time_file_name}/"
    # blobs = list_blobs_with_prefix(bucket_name, prefix, "ext")
    # print(f"Found {len(blobs)} blobs with prefix '{prefix}' in bucket '{bucket_name}'.")
    #
    # # Concat all data
    # for blob_name in blobs:
    #     # Download the blob into memory
    #     csv_bytes = download_blob_into_memory(bucket_name, blob_name)
    #
    #     # Read the CSV bytes into a DataFrame
    #     s = io.BytesIO(csv_bytes)
    #     tmp_df = pd.read_csv(s, encoding="utf-8", sep=",")
    #     print(f"Read data shape: {tmp_df.shape} from {blob_name}")
    #
    #     # Concatenate the DataFrame
    #     df = pd.concat([df, tmp_df], ignore_index=True)
    #
    # print(f"Transformed data shape: {df.shape}")
    # print(df.head())
    # print(df.info())
    # print(df.dtypes)
    #
    # # format to str
    # df["vinyl_format"] = df["vinyl_format"].astype(str)
    # df["vinyl_price"] = df["vinyl_price"].astype(str)
    #
    # # save parquet file
    # df.to_parquet("new_data_test.parquet", index=False)
    # return

    # read the parquet file
    df = pd.read_parquet("new_data_test.parquet")
    print(f"Transformed data shape: {df.shape}")

    #
    # remove Unnamed: 0
    df = df.loc[:, ~df.columns.str.contains("Unnamed")]

    # update vinyl_format
    df = update_format(df)

    # update vinyl_price and vinyl_currency
    df = update_price_currency(df)

    #
    # if vinyl_ref is null, set the title
    df["vinyl_reference"] = df["vinyl_reference"].fillna(df["vinyl_title"])

    #
    # convart date to datetime
    if "date_extract" in df.columns:
        df["date_extract"] = pd.to_datetime(df["date_extract"], errors="coerce")
        df["date_extract"] = df["date_extract"].dt.strftime("%Y-%m-%d %H:%M:%S")

    #
    print(df.info())
    print(df.head())

    save_file(
        df=df,
        file_name="trf_all_shops",
        bucket_name=bucket_name,
        time_file_name=time_file_name,
    )
