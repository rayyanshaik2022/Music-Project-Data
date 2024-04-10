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

def save_lyrics(file, genius, limit=0.2, output_dir="lyrics", debug=True):
    with open(file, "r") as json_file:
        data = json.load(json_file)

    lyrics = {}
    missing = []
    failures = 0
    success = 0

    save_at = 25

    for year in data:

        print(f"[*] Finding lyrics for year {year}")

        songs = data[year]
        for title, artist in songs:
            song_lyrics = fetch_lyrics(title, artist, genius)

            # Try again w/ different params
            if not song_lyrics:
                song_lyrics = fetch_lyrics(title, artist, genius)

            if not song_lyrics:
                missing.append([title, artist])
                if (debug):
                    print(f"[!] Search failed for {title} by {artist}")
                failures += 1

                with open(f"{output_dir}/missing.json", "w") as json_file:
                    json.dump({"missing": missing}, json_file)
               
            else:
                success += 1
                lyrics[f"{title} by {artist}"] = song_lyrics
        
            if success % save_at == 0:
                
                if (debug):
                    print(f"[+] {success} song lyrics found.")
            
                with open(f"{output_dir}/raw_data.json", "w") as json_file:
                    json.dump(lyrics, json_file)

            time.sleep(limit)

        with open(f"{output_dir}/raw_data.json", "w") as json_file:
            json.dump(lyrics, json_file)

        if debug:
            print(f"> Saved lyrics for songs charting in {year}")
            print(f"> Data saved in {output_dir}/{file}")
    
    print(f"[!] Total lyrics searches failed: {failures}")
    print(f"[+] Total lyrics searches completed: {success}")

#charts_file = "charts/data.json"
#save_lyrics(charts_file, limit=0.25)

#print(fetch_lyrics("Coming Home", "Diddy - Dirty Money"))