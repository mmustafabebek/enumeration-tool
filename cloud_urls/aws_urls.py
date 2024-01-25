import requests
from colorama import Fore, Style

# Function to check accessibility of AWS S3 bucket URLs
def check_aws_urls(bucket_name, regions, timeout):
    # Generate AWS S3 bucket base URLs for specified regions
    aws_base_urls = [f'https://{bucket_name}.s3.{region}.amazonaws.com' for region in regions] + [f'https://{bucket_name}.s3-{region}.amazonaws.com' for region in regions]
    accessible_urls = []
    inaccessible_urls = []

    for url in aws_base_urls:
        try:
            # Send a HEAD request to the URL with a specified timeout
            response = requests.head(url, timeout=timeout)
            if response.status_code == 200:
                accessible_urls.append(url)
            elif response.status_code == 403:
                print(Fore.RED + f"There is an S3 bucket ({url}), but it is not accessible because it is private." + Style.RESET_ALL)
                print("")
            else:
                inaccessible_urls.append(url)
        except requests.RequestException:
            inaccessible_urls.append(url)

    return accessible_urls, inaccessible_urls
