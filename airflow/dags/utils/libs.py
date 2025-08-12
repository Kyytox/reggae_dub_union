import pandas as pd

from utils.utils_gcp_storage import upload_blob, delete_blob


def save_file(
    df: pd.DataFrame, file_name: str, bucket_name: str, time_file_name: str
) -> None:
    """
    Save DataFrame to GCP Storage

    Args:
        df (pd.DataFrame): DataFrame to save
        file_name (str): name of file
        bucket_name (str): name of the GCP Storage bucket
        time_file_name (str): timestamp for file naming
    """
    path_file = f"extract_{time_file_name}/{file_name}.csv"
    upload_blob(bucket_name=bucket_name, df=df, destination_blob_name=path_file)


def format_path_file(time_file_name: str, prefix_file: str, file_name: str) -> str:
    """
    Format the path for the file in GCP Storage.

    Args:
        time_file_name (str): Timestamp for file naming.
        prefix_file (str): Prefix for the file path.
        file_name (str): Name of the file.


    Returns:
        str: Formatted path for the file.
    """
    return f"extract_{time_file_name}/{prefix_file}_{file_name}.csv"


def get_shops_links(df_shops: pd.DataFrame) -> list:
    """
    Get links for all shops from the DataFrame.

    Args:
        df_shops (pd.DataFrame): DataFrame containing shop information.

    Returns:
        list: List of URLs for all shops.
    """
    if "shop_link" not in df_shops.columns:
        raise ValueError("DataFrame does not contain 'shop_link' column")

    lst_urls = df_shops["shop_link"].dropna().tolist()

    if not lst_urls:
        raise ValueError("No links found in the DataFrame")

    return lst_urls
