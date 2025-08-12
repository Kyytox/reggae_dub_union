from google.cloud import storage

from airflow.models import Variable


def upload_blob(bucket_name, df, destination_blob_name):
    """
    Uploads a file to the bucket.

    Args:
        bucket_name (str): The name of the bucket to upload to.
        source_file_name (str): The path to the file to upload.
        destination_blob_name (str): The name of the blob in the bucket.
    """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    generation_match_precondition = 0

    blob.upload_from_string(
        df.to_csv(), "text/csv", if_generation_match=generation_match_precondition
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

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(blob_name)
    contents = blob.download_as_bytes()

    print(f"Blob {blob_name} downloaded from bucket {bucket_name}.")

    return contents


def delete_blob(bucket_name, blob_name):
    """
    Deletes a blob from the bucket.

    Args:
        bucket_name (str): The name of the bucket to delete from.
        blob_name (str): The name of the blob to delete.
    """

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    generation_match_precondition = None

    blob.reload()  # Fetch blob metadata to use in generation_match_precondition.
    generation_match_precondition = blob.generation

    blob.delete(if_generation_match=generation_match_precondition)

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

    storage_client = storage.Client()

    # List blobs with the specified prefix and delimiter
    print(f"List blobs in {bucket_name} with '{prefix}' and delimiter '{delimiter}'.")
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)

    # Stock the blobs and prefixes
    return [
        blob.name
        for blob in blobs
        if (
            blob.name.split("/")[-1].startswith(start_string)
            and blob.name.endswith(".csv")
        )
    ]
