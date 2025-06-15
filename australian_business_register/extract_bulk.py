from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import os
import time

def setup_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def get_zip_download_links(driver, dataset_url):
    driver.get(dataset_url)
    time.sleep(5)  # wait for page to fully load
    soup = BeautifulSoup(driver.page_source, "html.parser")

    download_links = []
    for a in soup.find_all("a", class_="download-button au-btn au-btn--secondary"):
        href = a.get("href")
        print(href)
        if href and href.endswith(".zip"):
            # Make absolute if needed
            if href.startswith("/"):
                href = "https://data.gov.au" + href
            download_links.append(href)

    return download_links

def download_zip_files(download_links, folder="abn_bulk_extract"):
    os.makedirs(folder, exist_ok=True)
    for url in download_links:
        filename = url.split("/")[-1]
        print(f"Downloading: {filename}")
        response = requests.get(url)
        file_path = os.path.join(folder, filename)
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Saved: {file_path}")

def main():
    dataset_url = "https://data.gov.au/dataset/ds-dga-5bd7fcab-e315-42cb-8daf-50b7efc2027e/details?q=abn"
    driver = setup_driver()
    try:
        download_links = get_zip_download_links(driver, dataset_url)
        print(f"Found {len(download_links)} .zip files.")
        download_zip_files(download_links)
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
