import pandas as pd

import nltk

nltk.download('vader_lexicon')


### Import the scraper functions
# from scraper.reviews_scraper import scrape_reviews

from app.scraper.reviews_scraper import scrape_reviews

#from app.scraper.reviews_scraper import scrape_reviews
from nltk.sentiment import SentimentIntensityAnalyzer

from tqdm import tqdm

sia = SentimentIntensityAnalyzer()



## define the model version
__version__ = "1.0.0"


### 1.  Get the book reviews as dataframe
def get_reviews_df(book_id):

    book_show_url = f"https://www.goodreads.com/book/show/{book_id}/reviews"
    # if the book_show_url is not valid, return None

    reviews_df = scrape_reviews(book_show_url)
    if reviews_df is None:
        return None

    return reviews_df

def get_top_reviews(book_id):
    reviews_count = 5
    url = f"https://www.goodreads.com/book/show/{book_id}/reviews"
    reviews_df = scrape_reviews(url)
    if reviews_df is None:
        return None
    if len(reviews_df) < reviews_count:
        return reviews_df.sort_values(by=['rating'], ascending=False)
    return reviews_df.sort_values(by=['rating'], ascending=False).head(reviews_count)

### Make a sentiment analysis for a given text

def get_polarity_scores(text):
   return sia.polarity_scores(text)

    