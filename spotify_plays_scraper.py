from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import os
import json
import time

from scrape_streams import scrape_streams

class SpotifyPlaysScraper:

    def __init__(self,  data_dir="data") -> None:
        
        self.driver = None
        self.data_dir = data_dir
        self.output_dir = f"{data_dir}/streams"

        self.songs_list = None

        self.init_driver()
        self.get_song_list()
        self.create_directories()

    
    def init_driver(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("log-level=3")

        path_to_extension = r'C:\Users\101pa\OneDrive\Documents\UPenn\5190 CIS\Music Project Data\chrome\1.57.0_12'
        chrome_options.add_argument('load-extension=' + path_to_extension)

        # Initialize the webdriver (for Chrome)
        driver = webdriver.Chrome(options=chrome_options)
        self.driver = driver
    
    def get_song_list(self):

        with open(f"{self.data_dir}/scraped/cleaned_data.json", "r") as json_file:
            data = json.load(json_file)
            songs = []

            for key in data:
                songs.extend(data[key])
            
            self.songs_list = songs
            print("[+] Opened and read all songs from file.")
    
    def create_directories(self):
        if not os.path.exists(self.data_dir):
            # Create the 'data' dir
            os.makedirs(self.data_dir)
            print("[+] Created 'data' directory")
        
        if not os.path.exists(self.output_dir):
            # Create the 'data' dir
            os.makedirs(self.output_dir)
            print("[+] Created 'data/streams' directory")

    def scrape(self, debug=False):

        counter = 0
        save_at = 5

        failures = 0

        streams = {}

        for song, artist in self.songs_list:

            try:
                song_streams = scrape_streams(self.driver, song, artist)
            except:
                if debug:
                    print(f"[!] Scrape failed for {song} by {artist}")      
                song_streams = {}

            if song_streams == {}:
                failures += 1

            streams[f"{song} by {artist}"] = song_streams

            counter += 1
            if counter % save_at == 0:
                with open(f"{self.output_dir}/raw_data.json", "w") as json_file:
                    json.dump(streams, json_file)
                
                if debug:
                    print(f"[+] Saved {counter} song stream counts!")
            
            # Don't overload the driver
            time.sleep(0.5)

        with open(f"{self.output_dir}/raw_data.json", "w") as json_file:
            json.dump(streams, json_file)

        print(f"[*] Finished with {failures} failures")

    def run(self):

        self.scrape()
        print("[+] Successfully scraped song streams!")

        print("=============================")
        print("[*] Completed streams scrape!")
        print("=============================")
if __name__ == "__main__":
    scraper = SpotifyPlaysScraper()
    scraper.run()