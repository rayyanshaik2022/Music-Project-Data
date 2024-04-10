import requests
from bs4 import BeautifulSoup
import json
import os


def scrape_wikipedia(url: str) -> [tuple]:
    # Fetch the HTML content of the Wikipedia page
    response = requests.get(url)
    
    # Check if request was successful
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the first <tbody> element
        tbody_element = soup.find_all('tbody')
        # Ensure we are taking the correct table (sometimes there are popups)
        tbody_element = tbody_element[len(tbody_element) - 2]
        
        # Extract the text content of each <tr> tag within <tbody> and store in an array
        tr_contents = []
        if tbody_element:
            tr_tags = tbody_element.find_all('tr')
            for tr_tag in tr_tags:
                # Find all the <td> tags within the <tr> tag
                td_tags = tr_tag.find_all('td')
                # Extract the text from each <td> tag and store in a tuple
                row_data = tuple(td.get_text() for td in td_tags)
                tr_contents.append(row_data)
            return tr_contents
        else:
            print("No <tbody> element found.")
            return None
    else:
        print("Failed to retrieve page:", response.status_code)
        return None

def scrape_by_range(year_range: (str)) -> [list]:

    print("> Starting wikipedia scrape")

    output = []
    for year in range(year_range[0], year_range[1] + 1):
        wikipedia_url = f'https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_{year}'
        content = scrape_wikipedia(wikipedia_url)
        if content:
            print(f"|---> Successfully scraped wikipedia for {year}")
            output.append(content)
        else:
            print(f"Error scraping {year} data.")

    return output

def clean_content(content: [tuple]):
    filter_by_empty = filter(lambda song_tup: len(song_tup) == 3, content)
    content = list(filter_by_empty)

    def clean_tuple(song_tup: tuple):
        number = int(song_tup[0])
        title = song_tup[1][1:-1]
        artist = song_tup[2].rstrip("\n")

        # Removed 'featured' artists
        if " featuring" in artist:
            before_featuring = artist.split(" featuring")[0]
            artist = before_featuring
        
        # Removes secondary artists (typically song is under first listed)
        if " and" in artist:
            before_and = artist.split(" and")[0]
            artist = before_and

        artist.strip()

        return (number, title, artist)

    # Todo, only include main artist and not featured ones
    # or 'X and Y'

    map_remove_quotations = map(clean_tuple , content)
    content = list(map_remove_quotations)

    return content

def save_to_json(data: dict, file: str, directory="charts"):
    # Check if the directory exists
    if not os.path.exists(directory):
        # Create the directory
        os.makedirs(directory)
        print(f"> Directory '{directory}' created.")
    else:
        print(f"> Directory '{directory}' already exist")

    with open(f"{directory}/data.json", "w") as json_file:
        json.dump(data, json_file)
    
    print(f"> Data saved in {directory}/{file}")

if __name__ == "__main__":
    year_range = (2010, 2023)
    content = scrape_by_range(year_range)
    processed_data = {}

    for i, data in enumerate(content):
        year = year_range[0] + i

        cleaned_data = clean_content(data)
        processed_data[year] = cleaned_data


    file = "data.json"
    save_to_json(processed_data, file)