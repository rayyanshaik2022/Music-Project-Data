from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

import os
import json
import re
import time
from difflib import get_close_matches, SequenceMatcher

from check_artists import process_name

chrome_options = Options()
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("log-level=3")

path_to_extension = r'C:\Users\101pa\OneDrive\Documents\UPenn\5190 CIS\Music Project Data\chrome\1.57.0_12'
chrome_options.add_argument('load-extension=' + path_to_extension)

# Initialize the webdriver (for Chrome)
driver = webdriver.Chrome(options=chrome_options)



artist = "Taylor Swift"
artist = process_name(artist)

url = f"https://kworb.net/itunes/artist/{artist}.html"
driver.get(url)
driver.implicitly_wait(1)

spotify_stats_ele = driver.find_element(by=By.LINK_TEXT, value="Spotify stats")
spotify_stats_ele.click()
driver.implicitly_wait(1)
time.sleep(1)

# Get current URL
current_url = driver.current_url

# extract artist's kworb id
start_index = current_url.find("artist/") + len("artist/")
end_index = current_url.find("_songs")

# Extract the artist ID substring
artist_id = current_url[start_index:end_index]

# Go to spotify chart history page
# Taylor Swift: https://kworb.net/spotify/artist/06HL4z0CvFAxyc27GXpf02.html

url = f"https://kworb.net/spotify/artist/{artist_id}.html"
driver.get(url)

# TODO: song should be from list
song = "Cruel Summer"

# Get elements with links
linked_text_list = driver.find_elements(by=By.TAG_NAME, value="a")

linked_text_list.sort(key=lambda x: SequenceMatcher(isjunk=None, a=song, b=x.text).ratio(), reverse=True)
best_match_text = linked_text_list[0]
print(f"Best match: {best_match_text.text}")
best_match_text.click()
driver.implicitly_wait(2)

streams_btn = driver.find_element(by=By.ID, value="streams")
streams_btn.click()
driver.implicitly_wait(1)

# Get table
table_ele = driver.find_element(by=By.TAG_NAME, value="tbody")
all_rows = table_ele.find_elements(by=By.TAG_NAME, value="tr")

value_rows = all_rows[3:]

# TODO : modify this as needed
results = {}

for row in value_rows:
    column_eles = row.find_elements(by=By.TAG_NAME, value="td")
    results[column_eles[0]] = {
        "Global" : column_eles[1].find_element(by=By.CLASS_NAME, value="s").text,
        "US" : column_eles[2].find_element(by=By.CLASS_NAME, value="s").text
    }

print(results)

# C
time.sleep(15)