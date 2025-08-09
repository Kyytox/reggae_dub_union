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


def list_blobs_with_prefix(bucket_name, prefix, start_string, delimiter=None):
    """
    Lists all the blobs in the bucket that begin with the prefix.

    Args:
        bucket_name (str): The name of the bucket to list blobs from.
        prefix (str): The prefix to filter blobs by.
        start_string (str): A string to start the listing from.
        delimiter (str, optional): A delimiter to restrict the results to only

    This can be used to list all blobs in a "folder", e.g. "public/".

    The delimiter argument can be used to restrict the results to only the
    "files" in the given "folder". Without the delimiter, the entire tree under
    the prefix is returned. For example, given these blobs:

        a/1.txt
        a/b/2.txt

    If you specify prefix ='a/', without a delimiter, you'll get back:

        a/1.txt
        a/b/2.txt

    However, if you specify prefix='a/' and delimiter='/', you'll get back
    only the file directly under 'a/':

        a/1.txt

    As part of the response, you'll also get back a blobs.prefixes entity
    that lists the "subfolders" under `a/`:

        a/b/
    """

    storage_client = storage.Client()

    # List blobs with the specified prefix and delimiter
    blobs = storage_client.list_blobs(bucket_name, prefix=prefix, delimiter=delimiter)

    # Stock the blobs and prefixes
    # return [blob.name for blob in blobs if blob.name.endswith(".csv")]
    return [
        blob.name
        for blob in blobs
        if (blob.name.endswith(".csv") and blob.name.startswith(start_string))
    ]
