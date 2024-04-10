import requests
import re
import json
import time

def has_artist(artist):
    url = f"https://kworb.net/itunes/artist/{artist}.html"

    try:
        response = requests.get(url)
        if response.status_code == 404:
            return True
        else:
            print(f"[!] Missing {artist}")
            return False
    except requests.RequestException as e:
        print(f"[!] Error finding {artist}")
        return False

def process_name(name):

    name = name.lower()

    # Remove spaces
    name = name.replace(" ", "")

    pattern = r"[^a-z0-9]"
    # Use re.sub() to replace the matched characters with an empty string
    name = re.sub(pattern, "", name)

    return name

def get_artists(input_file) -> set:

    with open(input_file, "r") as json_file:
        data = json.load(json_file)

    artists = {}

    for year in data:
        for song, artist in data[year]:
            artists[artist] = process_name(artist)

    print(f"[*] Total artists: {len(artists)}")

    return artists

def find_kworb_missing_artists(artists: dict):

    missing_artists = set()

    for name in artists:

        if not has_artist(name):
            missing_artists.add(name)

    return missing_artists

if __name__ == "__main__":

    input_file = "data/scraped/cleaned_data.json"
    artists = get_artists(input_file)

    missing = find_kworb_missing_artists(artists)

    print(missing)
    print(f"Missing artists: {len(missing)}")
    
