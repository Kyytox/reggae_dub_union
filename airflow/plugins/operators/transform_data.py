import io
import re
import pandas as pd

# from helpers.utils_gcp_storage import download_blob_into_memory, list_blobs_with_prefix

from airflow.models import Variable


def transform_data(bucket_name: str, time_file_name: str):
    """
    Transform data from a all shops present in folder extract_{time_file_name} in GCP Storage.

    Args:
        bucket_name (str): The name of the GCP Storage bucket to upload the transformed data.
        time_file_name (str): The timestamp used for naming the file.
    """

    # df = pd.DataFrame()

    # # Get the list of files with prefix
    # prefix = f"extract_{time_file_name}/"
    # blobs = list_blobs_with_prefix(bucket_name, prefix)
    # print(f"Found {len(blobs)} blobs with prefix '{prefix}' in bucket '{bucket_name}'.")

    # # Concat all data
    # for blob_name in blobs:
    #     # Download the blob into memory
    #     csv_bytes = download_blob_into_memory(bucket_name, blob_name)

    #     # Read the CSV bytes into a DataFrame
    #     s = io.BytesIO(csv_bytes)
    #     tmp_df = pd.read_csv(s, encoding="utf-8", sep=",")
    #     print(f"Read data shape: {tmp_df.shape} from {blob_name}")

    #     # Concatenate the DataFrame
    #     df = pd.concat([df, tmp_df], ignore_index=True)

    # print(f"Transformed data shape: {df.shape}")
    # print(df.head())
    # print(df.info())
    # print(df.dtypes)

    # for value in df["vinyl_price"].unique():
    #     print(f"vinyl_price: {value}")

    # # format to str
    # df["format_vinyl"] = df["format_vinyl"].astype(str)
    # df["vinyl_price"] = df["vinyl_price"].astype(str)

    # save parquet file
    # df.to_parquet("data_test.parquet", index=False)

    # read the parquet file
    df = pd.read_parquet("data_test.parquet")
    print(f"Transformed data shape: {df.shape}")
    print(df.head())

    #
    #
    # remove Unnamed: 0
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    #
    #
    # Upper format_vinyl
    df["format_vinyl"] = df["format_vinyl"].str.upper()
    print(f"format_vinyl: {[value for value in df['format_vinyl'].unique()]}")

    #
    #
    # replace , with . for regex
    df["vinyl_price"] = df["vinyl_price"].replace(",", ".", regex=True)

    # keep only special characters
    # Create vinyl_currency column before cleaning the vinyl_price column
    # df["vinyl_currency"] = (
    #     df["vinyl_price"]
    #     .apply(lambda x: re.sub(r"[^\D]", "", str(x)) if pd.notna(x) else "")
    #     .replace("(TTC)", "")
    #     .replace(",", "")
    #     .replace(".", "")
    # )
    # df["vinyl_currency"] = df["vinyl_currency"].str.strip()
    df["vinyl_currency"] = (
        df["vinyl_price"]
        .astype(str)
        .str.replace(r"[\d.,\s]+|\(TTC\)", "", regex=True)
        .str.strip()
    )

    # split vinyl_price
    # Convert vinyl_price to string and remove non-numeric characters
    df["vinyl_price"] = (
        df["vinyl_price"].astype(str).str.replace(r"[^\d.]", "", regex=True)
    )
    # Convert to float
    df["vinyl_price"] = pd.to_numeric(df["vinyl_price"], errors="coerce")
    print(df[["vinyl_price", "vinyl_currency"]].head(50))

    #
    #
    # if vinyl_ref is null, set the title
    df["vinyl_ref"] = df["vinyl_ref"].fillna(df["vinyl_title"])

    #
    #
    # convart date to datetime
    if "date_extract" in df.columns:
        df["date_extract"] = pd.to_datetime(df["date_extract"], errors="coerce")
        df["date_extract"] = df["date_extract"].dt.strftime("%Y-%m-%d %H:%M:%S")

    #
    #
    print(df.info())
    print(df.dtypes)
    print(df.head())


transform_data("your-bucket-name", "20250727_05")
