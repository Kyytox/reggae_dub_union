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

    # Optional: set a generation-match precondition to avoid potential race conditions
    # and data corruptions. The request to upload is aborted if the object's
    # generation number does not match your precondition.
    generation_match_precondition = 0

    blob.upload_from_string(
        df.to_csv(), "text/csv", if_generation_match=generation_match_precondition
    )

    print(f"File {destination_blob_name} uploaded to {bucket_name}.")


def download_blob_into_memory(bucket_name, blob_name):
    """Downloads a blob into memory."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your GCS object
    # blob_name = "storage-object-name"

    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    # Construct a client side representation of a blob.
    # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
    # any content from Google Cloud Storage. As we don't need additional data,
    # using `Bucket.blob` is preferred here.
    blob = bucket.blob(blob_name)
    contents = blob.download_as_bytes()

    print(f"Blob {blob_name} downloaded from bucket {bucket_name}.")

    return contents


def list_blobs_with_prefix(bucket_name, prefix, delimiter=None):
    """
    Lists all the blobs in the bucket that begin with the prefix.

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
    return [blob.name for blob in blobs if blob.name.endswith(".csv")]
