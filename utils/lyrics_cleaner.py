import json
import re

def remove_invalid_chars(sentence):
     pattern = r'[^\x20-\x7E]'

     cleaned_sentence = re.sub(r'[^\x20-\x7E]', '', sentence)
     return cleaned_sentence
     
def remove_number_embed(sentence):
    # Define a regular expression pattern to match the number followed by 'Embed' at the end of the string
    pattern = r'\d+Embed$'
    
    # Use re.sub() to replace the matched pattern with an empty string
    cleaned_sentence = re.sub(pattern, '', sentence)
    
    return cleaned_sentence

def clean_data(file, output_file):
    with open(file, "r") as json_file:
        data = json.load(json_file)

    for song in data:
        lyrics = data[song]

        # Remove first element (usually jumbled text)
        lyrics = lyrics[1:]
        for i, line in enumerate(lyrics):
            lyrics[i] = remove_invalid_chars(line)

        # Remove empty lines
        lyrics = [elem for elem in lyrics if elem != ""]

        #Fix 'Embed' on last line
        lyrics[-1] = remove_number_embed(lyrics[-1])

        # Re insert
        data[song] = lyrics
    
    # Save data
    with open(f"{output_file}", "w") as json_file:
            json.dump(data, json_file)

if __name__ == "__main__":
    input_file = "lyrics/missing_data.json"
    output_file = "lyrics/clean_missing_data.json"
    clean_data(input_file, output_file)