# Predicting the degree of virality of trending pop songs
By Rayyan Shaik, Esther Amao, Helen Nguyen 

## Our Goal: Predict how viral a trending song will be based on its lyrics
Our Neural Network's results:
- Accuracy: 68%
- F1 Scores: 48%, 77%, 0% for classes 0, 1 and 2 respectively

## Link to project presentation slides
<https://docs.google.com/presentation/d/1LOISIGj1PhIdwS4g1bRxUfjqIPT69dUa0159Eut3wM0/edit#slide=id.g2dc43245a29_0_255>

# About this Respository

This repository contains the code required to scrape the following:
- List of pops songs (names & artists) by year
- Lyrics and lyrics meta-data per song
- Weekly streaming data (global & US) per song 

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
