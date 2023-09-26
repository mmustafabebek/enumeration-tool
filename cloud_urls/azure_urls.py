import requests

def check_azure_urls(bucket_name, timeout):
    azure_blob_url = f'https://{bucket_name}.blob.core.windows.net'
    try:
        response = requests.head(azure_blob_url, timeout=timeout)
        if response.status_code == 200:
            return [azure_blob_url], []
        elif response.status_code == 403:
            print("There is such a blob bucket ({azure_blob_url}), but we cannot access it because it is private.")
        else:
            return [], [azure_blob_url]
    except requests.RequestException:
        return [], [azure_blob_url]
