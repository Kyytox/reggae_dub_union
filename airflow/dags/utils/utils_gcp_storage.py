from airflow import models
from airflow.providers.google.cloud.hooks.gcs import GCSHook


def upload_blob(bucket_name, df, destination_blob_name):
    """
    Uploads a file to the bucket.

    Args:
        bucket_name (str): The name of the bucket to upload to.
        source_file_name (str): The path to the file to upload.
        destination_blob_name (str): The name of the blob in the bucket.
    """

    # get variables
    conn_id = models.Variable.get("GCP_STORAGE_CONN")

    # use GCSHook to upload the file
    hook = GCSHook(gcp_conn_id=conn_id)
    hook.upload(
        bucket_name=bucket_name,
        object_name=destination_blob_name,
        data=df.to_csv(),
        mime_type="text/csv",
        encoding="utf-8",
    )

    print(f"File {destination_blob_name} uploaded to {bucket_name}.")


def download_blob_into_memory(bucket_name, blob_name):
    """Downloads a blob into memory.

    Args:
        bucket_name (str): The name of the bucket to download from.
        blob_name (str): The name of the blob to download.

    Returns:
        bytes: The contents of the blob as bytes.
    """

    # get variables
    conn_id = models.Variable.get("GCP_STORAGE_CONN")

    # use GCSHook to download the file
    hook = GCSHook(gcp_conn_id=conn_id)
    contents = hook.download(bucket_name=bucket_name, object_name=blob_name)

    print(f"Blob {blob_name} downloaded from bucket {bucket_name}.")

    return contents


def delete_blob(bucket_name, blob_name):
    """
    Deletes a blob from the bucket.

    Args:
        bucket_name (str): The name of the bucket to delete from.
        blob_name (str): The name of the blob to delete.
    """
    # get variables
    conn_id = models.Variable.get("GCP_STORAGE_CONN")

    # use GCSHook to delete the file
    hook = GCSHook(gcp_conn_id=conn_id)
    hook.delete(bucket_name=bucket_name, object_name=blob_name)

    print(f"Blob {blob_name} deleted.")


def list_blobs_with_prefix(
    bucket_name: str, prefix: str, start_string: str, delimiter=None
):
    """
    Lists all the blobs in the bucket that begin with the prefix.

    Args:
        bucket_name (str): The name of the bucket to list blobs from.
        prefix (str): The prefix to filter blobs by.
        start_string (str): A string to start the listing from.
        delimiter (str, optional): A delimiter to restrict the results to only


    doc: https://cloud.google.com/storage/docs/listing-objects?hl=fr&authuser=1#storage-list-objects-python
    """
    # get variables
    conn_id = models.Variable.get("GCP_STORAGE_CONN")

    # use GCSHook to list the files
    hook = GCSHook(gcp_conn_id=conn_id)
    blobs = hook.list(bucket_name=bucket_name, prefix=prefix)
    print(f"Blobs: {blobs}")

    # Stock the blobs and prefixes
    return [
        blob
        for blob in blobs
        if (blob.split("/")[-1].startswith(start_string) and blob.endswith(".csv"))
    ]
