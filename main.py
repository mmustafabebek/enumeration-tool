import concurrent.futures
import time
from cloud_regions.aws_regions import REGIONS
from restricts import aws_is_valid_bucket_name, azure_is_valid_blob_name, gcp_is_valid_storage_name
from cloud_urls.aws_urls import check_aws_urls
from cloud_urls.azure_urls import check_azure_urls
from cloud_urls.gcp_urls import check_gcp_urls
from arg_handler import parse_args

CONNECTIONS = 100
TIMEOUT = 5


def get_user_input():
    args = parse_args()

    name = args.name
    keyword = args.keyword

    while True:
        user_input = input("Please enter a name: ")
        user_input = user_input.strip()

        is_aws_valid = aws_is_valid_bucket_name(user_input)
        is_azure_valid = azure_is_valid_blob_name(user_input)
        is_gcp_valid = gcp_is_valid_storage_name(user_input)

        results = {
            "AWS": is_aws_valid,
            "Azure": is_azure_valid,
            "GCP": is_gcp_valid
        }

        valid_providers = [provider for provider, is_valid in results.items() if is_valid]
        invalid_providers = [provider for provider, is_valid in results.items() if not is_valid]

        if valid_providers:
            print(f"Valid input for: {', '.join(valid_providers)}")
        if invalid_providers:
            print(f"Invalid input for: {', '.join(invalid_providers)}")

        if valid_providers:
            return user_input, valid_providers
        else:
            print("Invalid input. Please enter a valid name for AWS, Azure, or GCP.")


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

    print(f'{provider} Accessible URLs ({len(accessible_urls[provider])}):')
    for url in accessible_urls[provider]:
        print(f'   {url}')

    print(f'{provider} Inaccessible URLs ({len(inaccessible_urls[provider])}):')
    for url in inaccessible_urls[provider]:
        print(f'   {url}')

    return time2 - time1


if __name__ == '__main__':
    name, providers = get_user_input()
    if name:
        total_time = 0
        for provider in providers:
            provider_time = fetch_web_pages(provider, name, TIMEOUT)
            total_time += provider_time
        print(f'Total time: {total_time:.2f} s')
