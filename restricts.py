import re

def aws_is_valid_bucket_name(bucket_name):

    if not 3 <= len(bucket_name) <= 63:
        print("Bucket name length must be between 3 and 63 characters.")
        return False


    if not re.match(r'^[a-zA-Z0-9]', bucket_name):
        print("Bucket name must start with a letter or number.")
        return False


    if '..' in bucket_name:
        print("Bucket name must not contain two adjacent periods.")
        return False


    if re.match(r'^\d+\.\d+\.\d+\.\d+$', bucket_name):
        print("Bucket name cannot be in the format of an IP address.")
        return False


    if bucket_name.startswith(('xn--', 'sthree-', 'sthree-configurator')):
        print("Bucket name cannot start with 'xn--', 'sthree-', or 'sthree-configurator'.")
        return False


    if bucket_name.endswith(('-s3alias', '--ol-s3')):
        print("Bucket name cannot end with '-s3alias' or '--ol-s3'.")
        return False


    if not re.match(r'^[a-z0-9.-]+$', bucket_name):
        print("Bucket name can only contain lowercase letters, numbers, periods, and hyphens.")
        return False

    return True

