import pandas as pd

from utils.utils_gcp_storage import upload_blob


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
