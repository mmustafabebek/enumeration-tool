import requests
from colorama import Fore, Style

def check_azure_urls(bucket_name, timeout):
    azure_blob_url = f'https://{bucket_name}.blob.core.windows.net'
    try:
        response = requests.head(azure_blob_url, timeout=timeout)
        if response.status_code == 200:
            return [azure_blob_url], []
        elif response.status_code == 403:
            print(Fore.RED + "There is such a blob bucket ({azure_blob_url}), but we cannot access it because it is private." + Style.RESET_ALL)
            print("")
        else:
            return [], [azure_blob_url]
    except requests.RequestException:
        return [], [azure_blob_url]
