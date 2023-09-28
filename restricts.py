import re

# Function to check if an AWS S3 bucket name is valid
def aws_is_valid_bucket_name(bucket_name):
    # Regular expression pattern to validate an AWS S3 bucket name
    pattern = r"^(?=.{3,63}$)(?!xn--|sthree-|sthree-configurator)(?!.*\.\.|.*-s3alias$|.*--ol-s3$)[a-z0-9][a-z0-9.-]*[a-z0-9]$"
    return bool(re.match(pattern, bucket_name))

# Function to check if an Azure Blob Storage blob name is valid
def azure_is_valid_blob_name(blob_name):
    # Regular expression pattern to validate an Azure Blob Storage blob name
    pattern = r"^(?!.*[/\.]{2,})[a-z0-9\.\-/]{1,1024}$"

    if re.match(pattern, blob_name):
        return True
    else:
        return False

# Function to check if a Google Cloud Storage bucket name is valid
def gcp_is_valid_storage_name(bucket_name):
    # Regular expression pattern to validate a Google Cloud Storage bucket name
    pattern = r"^(?!goog)(?!.*\.goog)(?!.*\.\d+\.\d+\.\d+\.\d+)(?!.*google)[a-z0-9][a-z0-9\._-]{1,61}[a-z0-9]$"

    if re.match(pattern, bucket_name):
        return True
    else:
        return False
