# How to use

## Required libraries
- selenium
- lyricsgenius
- python-dotenv

## Required API Keys
- Genius API Key required
  - [https://docs.genius.com/](https://docs.genius.com/)

## Running Files

- Simplying running `main.py` via `py main.py` or `python3 main.py` should be sufficient to begin a general
scrape
- In `main.py` you can adjust the `years` variable range to change the range of years queried (if playlists within the range exist).

- All scraping functions run their own data-cleaning utilities ensure all the data is standardized and usable



### Scrape Songs List
- Run the file `song_scraper.py`
  - Adjust the variable `year_range` to scrape the desired range of playlists for songs

### Scrape Lyrics
- Run the file `lyrics_scraper.py`
  - `config['TOKEN']` needs to be set to your [Genius.com](Genius.com) API key

### Spotify Streams
- Run the file `spotify_plays_scraper.py`
