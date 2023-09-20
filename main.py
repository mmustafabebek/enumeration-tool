import concurrent.futures
import time
from cloud_regions.aws_regions import REGIONS
from restricts import aws_is_valid_bucket_name
from cloud_urls.aws_urls import check_aws_urls
from cloud_urls.azure_urls import check_azure_urls
from cloud_urls.gcp_urls import check_gcp_urls

CONNECTIONS = 100
TIMEOUT = 5


def get_user_input():
    while True:
        user_input = input("Please enter a bucket name: ")
        if aws_is_valid_bucket_name(user_input):
            return user_input.strip()
        else:
            print("Invalid input. Please enter a valid bucket name.")


def fetch_web_pages(bucket_name, timeout):
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        time1 = time.time()
        accessible_urls = {"AWS": [], "Azure": [], "GCP": []}
        inaccessible_urls = {"AWS": [], "Azure": [], "GCP": []}

        aws_accessible, aws_inaccessible = check_aws_urls(bucket_name, REGIONS, timeout)
        azure_accessible, azure_inaccessible = check_azure_urls(bucket_name, timeout)
        gcp_accessible, gcp_inaccessible = check_gcp_urls(bucket_name, timeout)

        accessible_urls["AWS"].extend(aws_accessible)
        inaccessible_urls["AWS"].extend(aws_inaccessible)
        accessible_urls["Azure"].extend(azure_accessible)
        inaccessible_urls["Azure"].extend(azure_inaccessible)
        accessible_urls["GCP"].extend(gcp_accessible)
        inaccessible_urls["GCP"].extend(gcp_inaccessible)

        time2 = time.time()

    print(f'Took {time2 - time1:.2f} s')

    for cloud_provider, urls in accessible_urls.items():
        print(f'{cloud_provider} Accessible URLs ({len(urls)}):')
        for url in urls:
            print(f'   {url}')

    for cloud_provider, urls in inaccessible_urls.items():
        print(f'{cloud_provider} Inaccessible URLs ({len(urls)}):')
        for url in urls:
            print(f'   {url}')


if __name__ == '__main__':
    bucket_name = get_user_input()
    if bucket_name:
        fetch_web_pages(bucket_name, TIMEOUT)
