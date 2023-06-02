from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import re
import pandas as pd

def scrape_reviews(url):
    # Configure ChromeOptions to use ChromeDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run ChromeDriver in headless mode (without opening the browser window)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Use ChromeDriverManager to automatically download the appropriate ChromeDriver
    driver = webdriver.Chrome(ChromeDriverManager(version="113.0.5672.63").install(), options=options)

    # Open the URL
    driver.get(url)

    # If the page still contains Loading... wait for the reviews to load
    waiting_time = 10
    while driver.page_source.find('Loading...') != -1:
        WebDriverWait(driver, waiting_time).until_not(EC.presence_of_element_located((By.CLASS_NAME, 'Loading')))
        source = driver.page_source
        waiting_time += 5


    reviews_element = driver.find_element(By.CLASS_NAME, 'ReviewsList')

    # Get the ReviewCards from the reviews element
    review_cards = reviews_element.find_elements(By.CLASS_NAME, 'ReviewCard')


    reviews = []
    for review_card in review_cards:
        #Get the reviewer name
        reviewer_name = review_card.find_element(By.CLASS_NAME, 'ReviewerProfile__name').text
        #Get the review text
        review_text = review_card.find_element(By.CLASS_NAME, 'TruncatedContent').text
        #Get the review rating
        #<section class="ReviewCard__row"><div class="ShelfStatus"><span aria-label="Rating 5 out of 5" role="img" class="RatingStars RatingStars__small"><span class="baseClass RatingStar--small"><svg viewBox="0 0 24 24" role="presentation"><path class="RatingStar__fill" d="M24 9.63469C24 9.35683 23.7747 9.13158 23.4969 9.13158H15.0892L12.477 1.34327C12.4269 1.19375 12.3095 1.0764 12.16 1.02625C11.8966 0.937894 11.6114 1.07983 11.523 1.34327L8.91088 9.13158H0.503157C0.33975 9.13158 0.186521 9.21094 0.0922364 9.3444C-0.0680877 9.57134 -0.0140806 9.88529 0.212865 10.0456L7.00408 14.8432L4.40172 22.6166C4.35092 22.7683 4.37534 22.9352 4.46749 23.066C4.6275 23.2932 4.94137 23.3476 5.16853 23.1876L12 18.3758L18.8317 23.183C18.9625 23.2751 19.1293 23.2994 19.281 23.2486C19.5445 23.1604 19.6865 22.8752 19.5983 22.6117L16.996 14.8432L23.7872 10.0456C23.9206 9.95133 24 9.7981 24 9.63469Z"></path></svg></span><span class="baseClass RatingStar--small"><svg viewBox="0 0 24 24" role="presentation"><path class="RatingStar__fill" d="M24 9.63469C24 9.35683 23.7747 9.13158 23.4969 9.13158H15.0892L12.477 1.34327C12.4269 1.19375 12.3095 1.0764 12.16 1.02625C11.8966 0.937894 11.6114 1.07983 11.523 1.34327L8.91088 9.13158H0.503157C0.33975 9.13158 0.186521 9.21094 0.0922364 9.3444C-0.0680877 9.57134 -0.0140806 9.88529 0.212865 10.0456L7.00408 14.8432L4.40172 22.6166C4.35092 22.7683 4.37534 22.9352 4.46749 23.066C4.6275 23.2932 4.94137 23.3476 5.16853 23.1876L12 18.3758L18.8317 23.183C18.9625 23.2751 19.1293 23.2994 19.281 23.2486C19.5445 23.1604 19.6865 22.8752 19.5983 22.6117L16.996 14.8432L23.7872 10.0456C23.9206 9.95133 24 9.7981 24 9.63469Z"></path></svg></span><span class="baseClass RatingStar--small"><svg viewBox="0 0 24 24" role="presentation"><path class="RatingStar__fill" d="M24 9.63469C24 9.35683 23.7747 9.13158 23.4969 9.13158H15.0892L12.477 1.34327C12.4269 1.19375 12.3095 1.0764 12.16 1.02625C11.8966 0.937894 11.6114 1.07983 11.523 1.34327L8.91088 9.13158H0.503157C0.33975 9.13158 0.186521 9.21094 0.0922364 9.3444C-0.0680877 9.57134 -0.0140806 9.88529 0.212865 10.0456L7.00408 14.8432L4.40172 22.6166C4.35092 22.7683 4.37534 22.9352 4.46749 23.066C4.6275 23.2932 4.94137 23.3476 5.16853 23.1876L12 18.3758L18.8317 23.183C18.9625 23.2751 19.1293 23.2994 19.281 23.2486C19.5445 23.1604 19.6865 22.8752 19.5983 22.6117L16.996 14.8432L23.7872 10.0456C23.9206 9.95133 24 9.7981 24 9.63469Z"></path></svg></span><span class="baseClass RatingStar--small"><svg viewBox="0 0 24 24" role="presentation"><path class="RatingStar__fill" d="M24 9.63469C24 9.35683 23.7747 9.13158 23.4969 9.13158H15.0892L12.477 1.34327C12.4269 1.19375 12.3095 1.0764 12.16 1.02625C11.8966 0.937894 11.6114 1.07983 11.523 1.34327L8.91088 9.13158H0.503157C0.33975 9.13158 0.186521 9.21094 0.0922364 9.3444C-0.0680877 9.57134 -0.0140806 9.88529 0.212865 10.0456L7.00408 14.8432L4.40172 22.6166C4.35092 22.7683 4.37534 22.9352 4.46749 23.066C4.6275 23.2932 4.94137 23.3476 5.16853 23.1876L12 18.3758L18.8317 23.183C18.9625 23.2751 19.1293 23.2994 19.281 23.2486C19.5445 23.1604 19.6865 22.8752 19.5983 22.6117L16.996 14.8432L23.7872 10.0456C23.9206 9.95133 24 9.7981 24 9.63469Z"></path></svg></span><span class="baseClass RatingStar--small"><svg viewBox="0 0 24 24" role="presentation"><path class="RatingStar__fill" d="M24 9.63469C24 9.35683 23.7747 9.13158 23.4969 9.13158H15.0892L12.477 1.34327C12.4269 1.19375 12.3095 1.0764 12.16 1.02625C11.8966 0.937894 11.6114 1.07983 11.523 1.34327L8.91088 9.13158H0.503157C0.33975 9.13158 0.186521 9.21094 0.0922364 9.3444C-0.0680877 9.57134 -0.0140806 9.88529 0.212865 10.0456L7.00408 14.8432L4.40172 22.6166C4.35092 22.7683 4.37534 22.9352 4.46749 23.066C4.6275 23.2932 4.94137 23.3476 5.16853 23.1876L12 18.3758L18.8317 23.183C18.9625 23.2751 19.1293 23.2994 19.281 23.2486C19.5445 23.1604 19.6865 22.8752 19.5983 22.6117L16.996 14.8432L23.7872 10.0456C23.9206 9.95133 24 9.7981 24 9.63469Z"></path></svg></span></span></div><span class="Text Text__body3"><a href="https://www.goodreads.com/review/show/3121973347">January 11, 2020</a></span></section>
        #Get the review rating from the aria-label
        rating_content = review_card.find_element(By.CLASS_NAME, 'ReviewCard__content').get_attribute('innerHTML')
        #review_rating = re.findall(r'\d+', rating_content)
        
        review_rating = re.findall(r'\d+', rating_content)[0]

        #print(review_rating)
     


        #Get the reviewer avatar
        avatar_content = review_card.find_element(By.CLASS_NAME, 'ReviewerProfile__avatar').get_attribute('innerHTML')
        reviewer_avatar_matches = re.findall(r'src="(.*?)"', avatar_content)
        if reviewer_avatar_matches:
            reviewer_avatar = reviewer_avatar_matches[0]
        else:
            reviewer_avatar = None


        review = {
            'user': reviewer_name,
            'avatar': reviewer_avatar,
            'text': review_text,
            'rating': review_rating
        }
        reviews.append(review)

     # Save reviews to a dataframe
    reviews_df = pd.DataFrame(reviews)
    
    driver.quit()

    return reviews_df

    

