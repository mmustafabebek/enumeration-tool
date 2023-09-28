import concurrent.futures
import time
from cloud_regions.aws_regions import REGIONS
from restricts import aws_is_valid_bucket_name, azure_is_valid_blob_name, gcp_is_valid_storage_name
from cloud_urls.aws_urls import check_aws_urls
from cloud_urls.azure_urls import check_azure_urls
from cloud_urls.gcp_urls import check_gcp_urls
from arg_handler import parse_args
from colorama import Fore, Style

# Maximum number of concurrent connections
CONNECTIONS = 100
# Timeout duration (in seconds) for checking web pages
TIMEOUT = 5

# Function to obtain user input
def get_user_input():
    args = parse_args()
    name = args.name
    keyword = args.keyword

    # Check if the provided name is valid for AWS, Azure, and GCP
    is_aws_valid = aws_is_valid_bucket_name(name)
    is_azure_valid = azure_is_valid_blob_name(name)
    is_gcp_valid = gcp_is_valid_storage_name(name)

    results = {
        "AWS": is_aws_valid,
        "Azure": is_azure_valid,
        "GCP": is_gcp_valid
    }

    valid_providers = [provider for provider, is_valid in results.items() if is_valid]
    invalid_providers = [provider for provider, is_valid in results.items() if not is_valid]

    if valid_providers:
        print("")
        print(Fore.BLUE + "*********************************************************************" + Style.RESET_ALL)
        print(Fore.BLUE + "ENUMERATION TOOL" + Style.RESET_ALL)
        print(Fore.BLUE + "*********************************************************************" + Style.RESET_ALL)
        print("")
        print(Fore.YELLOW + "Scanning..." + Style.RESET_ALL)
        print("")
        print(Fore.GREEN + f"Valid input for: {', '.join(valid_providers)}" + Style.RESET_ALL)
        print("")
    if invalid_providers:
        print(Fore.RED + f"Invalid input for: {', '.join(invalid_providers)}" + Style.RESET_ALL)
        print("")
    if valid_providers:
        return name, valid_providers
    else:
        print(Fore.RED + "Invalid input. Please enter a valid name for AWS, Azure, or GCP." + Style.RESET_ALL)
        exit(1)

# Function to fetch web pages in parallel
def fetch_web_pages(provider, name, timeout):
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        time1 = time.time()
        accessible_urls = {"AWS": [], "Azure": [], "GCP": []}
        inaccessible_urls = {"AWS": [], "Azure": [], "GCP": []}

        if provider == "AWS":
            aws_accessible, aws_inaccessible = check_aws_urls(name, REGIONS, timeout)
            accessible_urls["AWS"].extend(aws_accessible)
            inaccessible_urls["AWS"].extend(aws_inaccessible)
        elif provider == "Azure":
            azure_accessible, azure_inaccessible = check_azure_urls(name, timeout)
            accessible_urls["Azure"].extend(azure_accessible)
            inaccessible_urls["Azure"].extend(azure_inaccessible)
        elif provider == "GCP":
            gcp_accessible, gcp_inaccessible = check_gcp_urls(name, timeout)
            accessible_urls["GCP"].extend(gcp_accessible)
            inaccessible_urls["GCP"].extend(gcp_inaccessible)

        time2 = time.time()

    print(Fore.BLUE + f'{provider} Accessible URLs ({len(accessible_urls[provider])}):' + Style.RESET_ALL)
    for url in accessible_urls[provider]:
        print(f'   {url}')

    print(Fore.BLUE + f'{provider} Inaccessible URLs ({len(inaccessible_urls[provider])}):' + Style.RESET_ALL)
    for url in inaccessible_urls[provider]:
        print(f'   {url}')

    return time2 - time1

# Main program
if __name__ == '__main__':
    name, providers = get_user_input()
    if name:
        total_time = 0
        for provider in providers:
            provider_time = fetch_web_pages(provider, name, TIMEOUT)
            total_time += provider_time
        print(f'Total time: {total_time:.2f} s')
