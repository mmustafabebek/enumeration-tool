import requests
from colorama import Fore, Style

def check_gcp_urls(bucket_name, timeout):
    google_storage_url = f'https://{bucket_name}.storage.googleapis.com'
    try:
        response = requests.head(google_storage_url, timeout=timeout)
        if response.status_code == 200:
            return [google_storage_url], []
        elif response.status_code == 403:
            print(Fore.RED + f"There is such a google storage ({google_storage_url}), but we cannot access it because it is private." + Style.RESET_ALL)
            print("")
            return [], [google_storage_url]
        else:
            return [], [google_storage_url]
    except requests.RequestException:
        return [], [google_storage_url]
