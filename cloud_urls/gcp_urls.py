import requests

def check_gcp_urls(bucket_name, timeout):
    google_storage_url = f'https://{bucket_name}.storage.googleapis.com'
    try:
        response = requests.head(google_storage_url, timeout=timeout)
        if response.status_code == 200:
            return [google_storage_url], []
        elif response.status_code == 403:
            print(f"There is such a google storage ({google_storage_url}), but we cannot access it because it is private.")
            return [], [google_storage_url]  # 403 hatası durumunda boş liste döndürün
        else:
            return [], [google_storage_url]
    except requests.RequestException:
        return [], [google_storage_url]
