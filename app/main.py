from fastapi import FastAPI
from pydantic import BaseModel


from app.model.model import get_reviews_df, get_top_reviews, get_polarity_scores,  __version__ as model_version
#from model.model import get_reviews_df, get_top_reviews, get_polarity_scores,  __version__ as model_version
#import uvicorn

app = FastAPI(
    title="Ohara-Bookshelf BOOK REVIEWS SCRAPER API",
    version="2.0.0",
    description="This is a simple API for scraping book reviews from Goodreads.com, using the book ID."
)



class BookIDInput(BaseModel):
    text: str


class BookReviewsOutput(BaseModel):
    reviews: list


class BookHighRatedReviewsOutput(BaseModel):
    top_reviews: list


@app.get("/")
def home():
    return {"health_check": "OK", "model_version": model_version}


@app.post("/book-reviews", response_model=BookReviewsOutput)
def book_reviews(book_id: BookIDInput):
    reviews_df = get_reviews_df(book_id.text)
    
    if reviews_df is None:
        return {"reviews": "There are no reviews for this book."}
    # Iterate through the reviews_df and add the sentiment analysis results
    for index, row in reviews_df.iterrows():
        polarity_scores = get_polarity_scores(row['text'])
        reviews_df.at[index, 'positivity'] = polarity_scores['pos']
        reviews_df.at[index, 'negativity'] = polarity_scores['neg']
        reviews_df.at[index, 'neutrality'] = polarity_scores['neu']
        reviews_df.at[index, 'compound'] = polarity_scores['compound']
        
        if polarity_scores['compound'] > 0:
            reviews_df.at[index, 'label'] = 'POSITIVE'
        elif polarity_scores['compound'] < 0:
            reviews_df.at[index, 'label'] = 'NEGATIVE'
        else:
            reviews_df.at[index, 'label'] = 'NEUTRAL'

    reviews_dict = reviews_df.to_dict('records')
    return {"reviews": reviews_dict}


@app.post("/book-high-rated-reviews", response_model=BookHighRatedReviewsOutput)
def book_high_rated_reviews(book_id: BookIDInput):
    high_rated_reviews_df = get_top_reviews(book_id.text)
    
    if high_rated_reviews_df is None:
        return {"top_reviews": "There are no reviews for this book."}
    # Iterate through the reviews_df and add the sentiment analysis results
    for index, row in high_rated_reviews_df.iterrows():
        polarity_scores = get_polarity_scores(row['text'])
        high_rated_reviews_df.at[index, 'positivity'] = polarity_scores['pos']
        high_rated_reviews_df.at[index, 'negativity'] = polarity_scores['neg']
        high_rated_reviews_df.at[index, 'neutrality'] = polarity_scores['neu']
        high_rated_reviews_df.at[index, 'compound'] = polarity_scores['compound']
        
        if polarity_scores['compound'] > 0:
            high_rated_reviews_df.at[index, 'label'] = 'POSITIVE'
        elif polarity_scores['compound'] < 0:
            high_rated_reviews_df.at[index, 'label'] = 'NEGATIVE'
        else:
            high_rated_reviews_df.at[index, 'label'] = 'NEUTRAL'
    
    high_rated_reviews_df = high_rated_reviews_df.to_dict('records')
    return {"top_reviews": high_rated_reviews_df}


# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=4000)
