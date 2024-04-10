import requests
import json
import os
import time

def fetch_lyrics(title, artist, genius):
    try:
        song = genius.search_song(title, artist)
        lyrics = song.lyrics.split("\n")
        return lyrics
    except:
        return False

def get_unfulfilled(file):
    with open(file, "r") as json_file:
        data = json.load(json_file)

    list_to_tup = [(item[0], item[1]) for item in data["missing"]]
    return set(list_to_tup)

if __name__ == "__main__":
    input_file = "lyrics/missing.json"
    rounds = 10
    unfulfilled = get_unfulfilled(input_file)

    lyrics = {}

    while len(unfulfilled) != 0:
        title, artist = unfulfilled.pop()

        song_lyrics = fetch_lyrics(title, artist)
        counter = 0
        
        while (not song_lyrics) and (counter < rounds):
            time.sleep(0.25)
            print(f"Retrying {title} by {artist} @ {counter}")
            song_lyrics = fetch_lyrics(title, artist)
            
            counter += 1
        
        if not song_lyrics:
            print(f"[!] Failed on {title} by {artist}") 

        lyrics[f"{title} by {artist}"] = song_lyrics

        time.sleep(0.25)

    print("[+] Saving data to file.")
    with open(f"lyrics/missing_data.json", "w") as json_file:
        json.dump(lyrics, json_file)