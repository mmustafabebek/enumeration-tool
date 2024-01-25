import requests
from colorama import Fore, Style

# Function to check accessibility of Google Cloud Storage URLs
def check_gcp_urls(bucket_name, timeout):
    # Generate the Google Cloud Storage URL
    google_storage_url = f'https://{bucket_name}.storage.googleapis.com'
    try:
        # Send a HEAD request to the URL with a specified timeout
        response = requests.head(google_storage_url, timeout=timeout)
        if response.status_code == 200:
            # Return the URL as accessible and an empty list for inaccessible URLs
            return [google_storage_url], []
        elif response.status_code == 403:
            # Print a message for a private bucket and return an empty list for accessible URLs
            print(Fore.RED + f"There is a Google Cloud Storage bucket ({google_storage_url}), but it is not accessible because it is private." + Style.RESET_ALL)
            print("")
            return [], [google_storage_url]
        else:
            # Return an empty list for accessible URLs and the URL as inaccessible
            return [], [google_storage_url]
    except requests.RequestException:
        # Return an empty list for accessible URLs and the URL as inaccessible in case of a request exception
        return [], [google_storage_url]
