from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import json
import time
import os


# Set Firefox options for running headless
chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("log-level=3")

# Set the path to the webdriver executable
# Make sure you have downloaded the geckodriver suitable for your browser (Firefox)
# and you have installed the Selenium library using `pip install selenium`
driver_path = "./geckodriver.exe"

# Initialize the webdriver (for Firefox)
driver = webdriver.Chrome(options=chrome_options)

def get_song_lyrics(title, artist, search="google lyrics"):

    # Better success with lowercase values for some reason
    original_title = title
    original_artist = artist
    title = title.lower()
    artist = artist.lower()

    try:
        # Open Google.com
        driver.get("https://www.google.com")

        # Find the search textarea by its name attribute (usually it's called "q" in Google)
        search_textarea = driver.find_element(by=By.NAME, value="q")

        # Click on the search textarea
        search_textarea.click()

        # You can also send keys to the search textarea (optional)
        search_textarea.send_keys(f"{title} by {artist} {search}")

        # Press Enter to submit the search query (optional)
        search_textarea.send_keys(Keys.RETURN)

        driver.implicitly_wait(0.3)

        # Find lyric box by its 'unique' class
    
        lyrics_box = driver.find_element(by=By.CLASS_NAME, value="sATSHe")

        all_spans = lyrics_box.find_elements(by=By.TAG_NAME, value="span")

        # Collect text from all spans
        lyrics_text = map(lambda ele: ele.text.strip(), all_spans)

        cleaned_lyrics = list(lyrics_text)[:-1]
        
        return cleaned_lyrics
    except:
        return False



def save_lyrics(file, output_dir="lyrics", debug=True):
    with open(file, "r") as json_file:
        data = json.load(json_file)

    lyrics = {}
    failures = 0
    success = 0

    if not os.path.exists(output_dir):
        # Create the directory
        os.makedirs(output_dir)
        print(f"> Directory '{output_dir}' created.")
    else:
        print(f"> Directory '{output_dir}' already exist")

    for year in data:
        songs = data[year]
        for _, title, artist in songs:
            song_lyrics = get_song_lyrics(title, artist)

            # Try again w/ different params
            if not song_lyrics:
                song_lyrics = get_song_lyrics(title, artist, "lyrics")

            if not song_lyrics:
    
                print(f"[!] Search failed for {original_title} by {original_artist}")
                failures += 1
            else:
                success += 1
                lyrics[f"{title} by {artist}"] = song_lyrics
        
            if success % 15 == 0:
                print(f"{success} song lyrics found.")

        with open(f"{output_dir}/data.json", "w") as json_file:
            json.dump(lyrics, json_file)

        if debug:
            print(f"> Saved lyrics for songs charting in {year}")
            print(f"> Data saved in {output_dir}/{file}")
    
    print(f"[!] Total failed: {failures}")

charts_file = "charts/data.json"
save_lyrics(charts_file)

# lyrics = get_song_lyrics("watermelon moonshine", "lainey wilson")
# lyrics2 = get_song_lyrics("poker face", "lady gaga")
# lyrics3 = get_song_lyrics("lucid dreams", "juice wrld")

# print(len(lyrics), len(lyrics2), len(lyrics3))