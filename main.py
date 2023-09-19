import concurrent.futures
import requests
import time
from cloud_providers.aws_regions import REGIONS
from restricts import aws_is_valid_bucket_name

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
    aws_base_urls = [f'https://{bucket_name}.s3.{region}.amazonaws.com' for region in REGIONS] + [f'https://{bucket_name}.s3-{region}.amazonaws.com' for region in REGIONS]
    azure_blob_url = f'https://{bucket_name}.blob.core.windows.net'
    google_storage_url = f'https://{bucket_name}.storage.googleapis.com'

    urls_to_check = aws_base_urls + [azure_blob_url, google_storage_url]

    def check_url(url):
        try:
            response = requests.head(url, timeout=timeout)
            return url, response.status_code == 200
        except requests.RequestException:
            return url, False

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = {executor.submit(check_url, url): url for url in urls_to_check}
        time1 = time.time()
        accessible_urls = {"AWS": [], "Azure": [], "GCP": []}
        inaccessible_urls = {"AWS": [], "Azure": [], "GCP": []}

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            url, is_accessible = future.result()
            if is_accessible:
                if url.startswith(f'https://{bucket_name}.s3'):
                    accessible_urls["AWS"].append(url)
                elif url.startswith(f'https://{bucket_name}.blob.core.windows.net'):
                    accessible_urls["Azure"].append(url)
                elif url.startswith(f'https://{bucket_name}.storage.googleapis.com'):
                    accessible_urls["GCP"].append(url)
            else:
                if url.startswith(f'https://{bucket_name}.s3'):
                    inaccessible_urls["AWS"].append(url)
                elif url.startswith(f'https://{bucket_name}.blob.core.windows.net'):
                    inaccessible_urls["Azure"].append(url)
                elif url.startswith(f'https://{bucket_name}.storage.googleapis.com'):
                    inaccessible_urls["GCP"].append(url)

            print(f'Checked {len(accessible_urls["AWS"]) + len(accessible_urls["Azure"]) + len(accessible_urls["GCP"]) + len(inaccessible_urls["AWS"]) + len(inaccessible_urls["Azure"]) + len(inaccessible_urls["GCP"])} URLs', end='\r')

        time2 = time.time()

    print(f'Took {time2 - time1:.2f} s')
    for cloud_provider, urls in accessible_urls.items():
        print(f'{cloud_provider} Accessible URLs: {len(urls)}')
    for cloud_provider, urls in inaccessible_urls.items():
        print(f'{cloud_provider} Inaccessible URLs: {urls}')


if __name__ == '__main__':
    bucket_name = get_user_input()
    if bucket_name:
        fetch_web_pages(bucket_name, TIMEOUT)
