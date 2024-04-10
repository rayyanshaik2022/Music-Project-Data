import unicodedata
import json
import os
import re

def unicode_to_ascii(text):
    # Normalize the text to decomposed form
    normalized_text = unicodedata.normalize('NFKD', text)
    # Replace characters that are not ASCII with their closest ASCII equivalents
    ascii_text = normalized_text.encode('ascii', 'ignore').decode('ascii')
    return ascii_text

def remove_text_in_parentheses_and_brackets(text):
    # Define a regular expression pattern to match text inside parentheses and brackets
    pattern = r'\s*\([^)]*\)|\s*\[[^\]]*\]'
    
    # Use re.sub() to replace the matched patterns with an empty string
    cleaned_text = re.sub(pattern, '', text)
    
    return cleaned_text.strip()  # Strip any leading/trailing whitespace

def clean_song(songs):

    output = []

    for title, artist in songs:

        # Clean title

        # Remove unknown unicode values
        title = unicode_to_ascii(title)
        title = remove_text_in_parentheses_and_brackets(title)
        title.rstrip()
        
        # Clean artist

        # just get first artist, split by ',' and '&'
        artist = artist.split(", ")[0]
        artist = artist.split("&")[0]
        artist = unicode_to_ascii(artist)
        artist.rstrip()

        output.append(
            (title, artist)
        )
    
    return output

def clean_songs(input_file, output_file):
    with open(input_file, "r") as json_file:
        data = json.load(json_file)
    
    for year in data:
        data[year] = clean_song(data[year])
    
    # Save
    with open(output_file, "w") as json_file:
        json.dump(data, json_file)

if __name__ == "__main__":

    input_file = "scraped/data.json"
    output_file = "scraped/cleaned_data.json"

    clean_songs(input_file, output_file)