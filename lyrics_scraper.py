import json
import time
import os

from utils.lyrics_aggregator import save_lyrics
from utils.requery_lyrics import get_unfulfilled, fetch_lyrics
from utils.lyrics_cleaner import clean_data

from lyricsgenius import Genius

class LyricsScraper:

    def __init__(self, config, data_dir="data") -> None:
        
        self.config = config

        self.data_dir = data_dir
        self.output_dir = f"{data_dir}/lyrics"

        self.create_directories()

    def create_directories(self):
        if not os.path.exists(self.data_dir):
            # Create the 'data' dir
            os.makedirs(self.data_dir)
            print("[+] Created 'data' directory")
        
        if not os.path.exists(self.output_dir):
            # Create the 'data' dir
            os.makedirs(self.output_dir)
            print("[+] Created 'data/lyrics' directory")

    def scrape(self, debug=False):

        genius = Genius(self.config["TOKEN"])
        genius.remove_section_headers = False
        genius.verbose = False

        input_file = f"{self.data_dir}/scraped/cleaned_data.json"
        output_dir = "data/lyrics"
        save_lyrics(input_file, genius, limit=0.25, output_dir=output_dir, debug=debug)
    
    def missing_scrape(self, debug=False):

        genius = Genius(self.config["TOKEN"])
        genius.remove_section_headers = False
        genius.verbose = False

        input_file = f"{self.output_dir}/missing.json"
        rounds = 10
        unfulfilled = get_unfulfilled(input_file)

        lyrics = {}

        while len(unfulfilled) != 0:
            title, artist = unfulfilled.pop()

            song_lyrics = fetch_lyrics(title, artist, genius)
            counter = 0
            
            while (not song_lyrics) and (counter < rounds):
                time.sleep(0.25)
                if debug:
                    print(f"[!] Retrying {title} by {artist} @ {counter}")
                song_lyrics = fetch_lyrics(title, artist, genius)
                
                counter += 1
            
            if not song_lyrics:
                print(f"[!] Failed on {title} by {artist}") 

            lyrics[f"{title} by {artist}"] = song_lyrics

            time.sleep(0.25)

        print("[+] Merging & saving data to file.")
        with open(f"{self.output_dir}/raw_data.json", "r") as json_file:
            raw_data = json.load(json_file)

        with open(f"{self.output_dir}/raw_data.json", "w") as json_file:
            
            if debug:
                print(f"[*] Unmerged data size: {len(raw_data.keys())}")
            
            lyrics.update(raw_data)

            if debug:
                print(f"[*] Merged data size: {len(lyrics.keys())}")
            
            json.dump(lyrics, json_file)

    def clean(self):

        input_file = f"{self.output_dir}/raw_data.json"
        output_file = f"{self.output_dir}/cleaned_data.json"

        clean_data(input_file, output_file)

    def run(self):

        #self.scrape(debug=True)
        print("[+] Successfully scraped song lyrics!")

        # Now re-attempt missing songs
        self.missing_scrape(debug=True)
        print("[+] Successfully requeried and scraped missing lyrics!")

        # Now lets clean the data
        self.clean()
        print("[+] Successfully cleaned song lyrics!")

        print("===============================")
        print("[*] Completed lyrics scrape & clean!")
        print("===============================")

if __name__ == "__main__":
    
    config = {
        "TOKEN" : "get token from env"
    }
    
    scraper = LyricsScraper(config)
    scraper.run()
