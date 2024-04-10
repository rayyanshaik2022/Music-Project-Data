from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import os

class SpotifyPlaysScraper:

    def __init__(self) -> None:
        pass

    
    def scrape(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("log-level=3")

        # Initialize the webdriver (for Chrome)
        driver = webdriver.Chrome(options=chrome_options)


if __name__ == "__main__":
    ...