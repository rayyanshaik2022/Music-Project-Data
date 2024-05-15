from song_scraper import SongScraper
from lyrics_scraper import LyricsScraper

from dotenv import dotenv_values

if __name__ == "__main__":

    env_variables = dotenv_values()

    config = {
        "TOKEN" : env_variables.get("GENIUS_TOKEN")
    }

    years = (2010, 2023)

    song_scraper = SongScraper(years)
    song_scraper.run()

    lyrics_scraper = LyricsScraper(config)
    lyrics_scraper.run()