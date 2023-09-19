import concurrent.futures
import requests
import time
from cloud_providers.aws_regions import REGIONS
from restricts import aws_is_valid_bucket_name
import itertools

CONNECTIONS = 100
TIMEOUT = 5

def get_user_input():
    while True:
        user_input = input("Please enter a bucket name: ")
        if aws_is_valid_bucket_name(user_input):
            return user_input.strip()
        else:
            print("Invalid input. Please enter a valid bucket name.")

def generate_bucket_name_variations(bucket_name):
    allowed_characters = "abcdefghijklmnopqrstuvwxyz0123456789.-"
    character_variations = itertools.product(allowed_characters, repeat=len(bucket_name))
    variations = [''.join(chars) for chars in character_variations]
    return variations

def fetch_web_pages(bucket_name, timeout):
    variations = generate_bucket_name_variations(bucket_name)
    urls = [f'https://{variation}.s3.{region}.amazonaws.com' or f'https://{variation}.s3-{region}.amazonaws.com' for region in REGIONS for variation in variations]

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
