import re

def aws_is_valid_bucket_name(bucket_name):
    pattern = r"^(?!xn--|sthree-|sthree-configurator)[a-zA-Z0-9][a-z0-9.-]{1,61}[a-z0-9](?<!-s3alias|--ol-s3)$"
    if re.match(pattern, bucket_name):
        return True
    else:
        print("Bucket name is not valid.")
        return False

def azure_is_valid_blob_name(blob_name):
        pattern = r"^(?!.*[/\.]{2,})[a-z0-9\.\-/]{1,1024}$"

        if re.match(pattern, blob_name):
            return True
        else:
            print("Invalid blob name.")
            return False

def gcp_is_valid_storage_name(bucket_name):
    pattern = r"^(?!goog)(?!.*\.goog)(?!.*\.\d+\.\d+\.\d+\.\d+)(?!.*google)[a-z0-9][a-z0-9\._-]{1,61}[a-z0-9]$"

    if re.match(pattern, bucket_name):
        return True
    else:
        print("Invalid Google Cloud Storage name.")
        return False
