import pandas as pd
import pytest
from dags.utils import utils_gcp_storage

bucket_name = "reg_dub_union_bucket"


def test_upload_blob():
    df = pd.DataFrame({"a": [1, 2]})
    utils_gcp_storage.upload_blob(bucket_name, df, "file.csv")


#
def test_download_blob_into_memory():
    utils_gcp_storage.download_blob_into_memory(bucket_name, "file.csv")


def test_delete_blob():
    utils_gcp_storage.delete_blob(bucket_name, "file.csv")
