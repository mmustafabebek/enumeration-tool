import requests

def check_azure_urls(bucket_name, timeout):
    azure_blob_url = f'https://{bucket_name}.blob.core.windows.net'
    try:
        response = requests.head(azure_blob_url, timeout=timeout)
        if response.status_code == 200:
            return [azure_blob_url], []
        else:
            return [], [azure_blob_url]
    except requests.RequestException:
        return [], [azure_blob_url]
