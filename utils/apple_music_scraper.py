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

def search_playlist(playlist, year):

    try:
        # Open Google.com
        driver.get("https://www.google.com")

        # Find the search textarea by its name attribute (usually it's called "q" in Google)
        search_textarea = driver.find_element(by=By.NAME, value="q")

        # Click on the search textarea
        search_textarea.click()

        # You can also send keys to the search textarea (optional)
        search_textarea.send_keys(f"{playlist} {year}")

        # Press Enter to submit the search query (optional)
        search_textarea.send_keys(Keys.RETURN)

        driver.implicitly_wait(1)

        # Get all h3 elements
        h3_elements = driver.find_elements(by=By.TAG_NAME, value="h3")
        if h3_elements:
            h3_elements[0].click()
        else:
            print(f"[!] No h3 elements found on the webpage for year {year}")
            return

        driver.implicitly_wait(6)

        # Get all songs names by classname
        songs = driver.find_elements(by=By.CLASS_NAME, value="songs-list-row__song-name-wrapper")
        if songs:
            result = [s.text.split("\n") for s in songs]
            return result
        else:
            print(f"[!] No songs found for {year}")
    except:
        pass

def search_range(playlist, years, output_dir):
    start, end = years

    results = {}

    for year in range(start, end + 1):
        out = search_playlist(playlist, year)
        results[year] = out

        print(f"[+] Saving songs for: {year}")
        save_results(results, output_dir)
        time.sleep(29)

    return results

def save_results(results, output_dir="scraped"):
    
    with open(f"{output_dir}/raw_data.json", "w") as json_file:
            json.dump(results, json_file)

if __name__ == "__main__":
    playlist = "apple music pop hits"
    years = (2010, 2023)
    output_dir = "data/scraped"
    
    results = search_range(playlist, years, output_dir)