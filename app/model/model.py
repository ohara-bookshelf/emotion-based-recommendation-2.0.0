import pandas as pd

### Import the scraper functions
from app.scraper.reviews_content import get_book_reviews_section, get_review_cards, get_all_reviews

import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer

from tqdm import tqdm

sia = SentimentIntensityAnalyzer()

## define the model version
__version__ = "1.0.0"


### 1.  Get the book reviews as dataframe
def get_reviews_df(book_id):

    book_show_url = f"https://www.goodreads.com/book/show/{book_id}"
    # if the book_show_url is not valid, return None
    if book_show_url is None:
        return None
    # if the reviews_content is empty, return None

    reviews_content = get_book_reviews_section(book_show_url)
    if reviews_content is None:
        return None
    review_cards = get_review_cards(reviews_content)
    if review_cards is None:
        return None
    reviews_df = pd.DataFrame(get_all_reviews(review_cards))
    if reviews_df.empty:
        return None
    # Convert the reviews_df to a table
    return reviews_df


def get_high_rated_reviews(book_id):
    # Get the reviews_df
    reviews_df = get_reviews_df(book_id)
    # if the reviews_df is empty, return None
    if reviews_df.empty:
        return "There are no reviews for this book."
    #if reviews_df length is less than 10, return the reviews_df
    if len(reviews_df) < 10:
        return reviews_df.sort_values(by=['rating'], ascending=False)
    return reviews_df.sort_values(by=['rating'], ascending=False).head(10)


### Make a sentiment analysis for a given text

def get_polarity_scores(text):
   
   return sia.polarity_scores(text)

    