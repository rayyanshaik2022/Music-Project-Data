import requests
import json
import os
import time

def get_genre(title, artist):

    formatted_title = title.replace(" ", "%20")
    formatted_artist = artist.replace(" ", "%20")
    # API endpoint URL
    url = f"https://api.musixmatch.com/ws/1.1/matcher.track.get?q_track={formatted_title}&q_artist={formatted_artist}&apikey={API_KEY}"
   #url = f"https://api.musixmatch.com/ws/1.1/matcher.track.get?q_track={'Grenade'}&q_artist={'Bruno Mars'}&apikey={API_KEY}"
    try:
        # Perform a GET request
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            # Do something with the data
            return data, (title, artist)
        else:
            print(f"Error: Unable to fetch data. Status code: {response.status_code}")
            return False
    except:
        return False

def is_genre(res, genre="Pop"):

    genre = genre.rstrip().lower()

    if not res:
        print(f"[!] Failed finding genre for <Unknown>")
        return False
    
    title, artist = res[1]
    res = res[0]

    print("HERE",res)
    found_genres = res["message"]["body"]["track"]["primary_genres"]["music_genre_list"]
    for genre_dict in found_genres:
        single_genre = genre_dict["music_genre"]["music_genre_name"].lower()

        if genre in single_genre:
            return True
    
    return False



title = "Lover"
artist = "Taylor Swift"

genre = get_genre(title, artist)
print(is_genre(genre))