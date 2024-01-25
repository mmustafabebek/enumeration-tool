import requests
from colorama import Fore, Style

# Function to check accessibility of Azure Blob Storage URLs
def check_azure_urls(bucket_name, timeout):
    # Generate the Azure Blob Storage URL
    azure_blob_url = f'https://{bucket_name}.blob.core.windows.net'
    try:
        # Send a HEAD request to the URL with a specified timeout
        response = requests.head(azure_blob_url, timeout=timeout)
        if response.status_code == 200:
            # Return the URL as accessible and an empty list for inaccessible URLs
            return [azure_blob_url], []
        elif response.status_code == 403:
            # Print a message for a private bucket and return an empty list for accessible URLs
            print(Fore.RED + f"There is an Azure Blob Storage bucket ({azure_blob_url}), but it is not accessible because it is private." + Style.RESET_ALL)
            print("")
        else:
            # Return an empty list for accessible URLs and the URL as inaccessible
            return [], [azure_blob_url]
    except requests.RequestException:
        # Return an empty list for accessible URLs and the URL as inaccessible in case of a request exception
        return [], [azure_blob_url]
