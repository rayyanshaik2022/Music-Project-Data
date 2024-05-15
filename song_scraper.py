from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import os

from utils.apple_music_scraper import search_range
from utils.song_list_cleaner import clean_songs

class SongScraper:

    def __init__(self, year_range, playlist="apple music pop hits", data_dir="data") -> None:
        
        self.data_dir = data_dir
        self.output_dir = f"{data_dir}/scraped"

        self.raw_data = None
        self.cleaned_data = None

        self.year_range = year_range
        self.playlist = playlist

        self.create_directories()

    def create_directories(self):

        if not os.path.exists(self.data_dir):
            # Create the 'data' dir
            os.makedirs(self.data_dir)
            print("[+] Created 'data' directory")

        if not os.path.exists(f"{self.data_dir}/scraped"):
            # Create the 'data/scraped' dir
            os.makedirs(f"{self.data_dir}/scraped")
            print("[+] Create 'data/scraped' directory")

    def scrape(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("log-level=3")

        # Initialize the webdriver (for Chrome)
        driver = webdriver.Chrome(options=chrome_options)

        search_range(
            self.playlist, 
            self.year_range, 
            self.output_dir
            )
    
    def clean(self):

        input_file = f"{self.output_dir}/raw_data.json"
        output_file = f"{self.output_dir}/cleaned_data.json"

        clean_songs(input_file, output_file)
    
    def run(self):

        self.scrape()
        print("[+] Successfully scraped songs list!")
        self.clean()
        print("[+] Successfully cleaned saved songs list!")

        print("===============================")
        print("[*] Completed song list scrape & clean!")
        print("===============================")

if __name__ == "__main__":
    year_range = (2010, 2023)
    scraper = SongScraper(year_range=year_range)
    scraper.run()