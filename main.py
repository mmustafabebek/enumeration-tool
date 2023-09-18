import concurrent.futures
import requests
import time
from cloud_providers.aws_regions import REGIONS

CONNECTIONS = 100000
TIMEOUT = 5

def get_user_input():
    user_input = input("Please enter a bucket name: ")
    return user_input.strip()

def fetch_web_pages(bucket_name, timeout):
    urls = [f'https://{bucket_name}.s3.{region}.amazonaws.com' or f'https://{bucket_name}.s3-{region}.amazonaws.com' for region in REGIONS]

    def check_url(url):
        try:
            response = requests.get(url, timeout=timeout)
            return url, response.status_code == 200
        except requests.RequestException:
            return url, False

    with concurrent.futures.ThreadPoolExecutor(max_workers=CONNECTIONS) as executor:
        future_to_url = {executor.submit(check_url, url): url for url in urls}
        time1 = time.time()
        accessible_urls = []
        inaccessible_urls = []

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            url, is_accessible = future.result()
            if is_accessible:
                accessible_urls.append(url)
            else:
                inaccessible_urls.append(url)

            print(f'Checked {len(accessible_urls) + len(inaccessible_urls)} URLs', end='\r')

        time2 = time.time()

    print(f'Took {time2 - time1:.2f} s')
    print(f'Accessible URLs: {len(accessible_urls)}')
    print(f'Inaccessible URLs: {len(inaccessible_urls)}')
    print("Accessible URLs: {}".format(accessible_urls))
    print("Inaccessible URLs: {}".format(inaccessible_urls))

if __name__ == '__main__':
    bucket_name = get_user_input()
    if bucket_name:
        fetch_web_pages(bucket_name, TIMEOUT)
