from bs4 import BeautifulSoup

import requests

#Regex usage
import re




### 1.  Get the book reviews section
def get_book_reviews_section(book_show_url):
   
    # Get the book page
    book_page = requests.get(book_show_url)
    # Create a BeautifulSoup object
    soup = BeautifulSoup(book_page.content, 'html.parser')
    # Get the reviews section
    reviews_content = soup.find_all('div', class_='ReviewsList')
    
    return  reviews_content


### 2. Get the reviews cards
def get_review_cards(reviews_content):
    review_cards = []
    reviewCards = reviews_content[1].find_all('article', class_='ReviewCard')
    for card in reviewCards:
        review_cards.append(card)
    return review_cards


### 3. Get all the reviews

def get_all_reviews(review_cards):

    reviews = []

    for card in review_cards:
        #Get the reviewer name
        reviewer_name = card.find('div', class_='ReviewerProfile__name').get_text()
        #Get the review text
        review_text = card.find('div', class_='TruncatedContent').get_text()
        #Get the review rating
        #review_content = card.find('span', class_='RatingStars RatingStars__small').get_text()
      
      
        #Get the review rating
        reviewRating = card.find('span', {'class': 'RatingStars RatingStars__small'})
        #Check if the review has a rating
        if reviewRating is None:
            return None
        ratingString = reviewRating['aria-label']  # extract the aria-label value
        rating = re.findall(r'\d+', ratingString)  # extract the number from the string
        
        #Return the first element of the list
        review_rating = rating[0]

        review = {
            'user': reviewer_name,
            'text': review_text,
            'rating': review_rating
        }
        
        reviews.append(review)

    return reviews

