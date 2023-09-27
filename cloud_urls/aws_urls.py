import requests
from colorama import Fore, Style

def check_aws_urls(bucket_name, regions, timeout):
    aws_base_urls = [f'https://{bucket_name}.s3.{region}.amazonaws.com' for region in regions] + [f'https://{bucket_name}.s3-{region}.amazonaws.com' for region in regions]
    accessible_urls = []
    inaccessible_urls = []

    for url in aws_base_urls:
        try:
            response = requests.head(url, timeout=timeout)
            if response.status_code == 200:
                accessible_urls.append(url)
            elif response.status_code == 403:
                print(Fore.RED + f"There is such an S3 bucket ({url}), but we cannot access it because it is private." + Style.RESET_ALL)
                print("")
            else:
                inaccessible_urls.append(url)
        except requests.RequestException:
            inaccessible_urls.append(url)

    return accessible_urls, inaccessible_urls
