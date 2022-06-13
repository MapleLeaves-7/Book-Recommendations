from bs4 import BeautifulSoup as bs
import requests
import re
import logging
# # selenium 4
# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from webdriver_manager.core.utils import ChromeType

# options = webdriver.ChromeOptions()
# options.add_argument('--ignore-certificate-errors')
# options.add_argument('--incognito')
# # options.add_argument('--headless')

# driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)


BASE_URL = "https://www.goodreads.com"

# ua = UserAgent()
headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0"}

# def get_book_links(link):
#     response = requests.get(BASE_URL + link)
#     soup = bs(response.content, "lxml")
#     books = soup.find_all("a", class_="bookTitle")
#     book_links = [b['href'] for b in books]
#     return book_links

def extract_element_text(element):
    text = element.get_text()
    return text.strip()

def extract_integer(text):
    # Regex to extract number
    regex = re.compile("(?:(?:\d+),)*\d+")
    number_text = regex.search(text)
    if not number_text:
        return None
    number_text = number_text.group()
    number = number_text.replace(",", "")
    return int(number)

def get_title(soup, is_beta=False):
    if is_beta:
        # New website format
        title_element = soup.find("h1", class_="Text Text__title1")
    else:
        # Old website format
        title_element = soup.find("h1", id="bookTitle")
        
    return extract_element_text(title_element)

def get_author(soup, is_beta=False):
    if is_beta:
        # New website format
        author_element = soup.find("span", class_="ContributorLink__name")
    else:
        # Old website format
        author_element = soup.find("a", class_="authorName").find("span")        
        
    return extract_element_text(author_element)

def get_description(soup, is_beta=False):
    if is_beta:
        # New website format
        content_element = soup.find("div", class_="BookPageMetadataSection__description").find("span", class_="Formatted")
    else:
        # Old website format
        content_element = soup.find("div", id="description")
        if content_element is None:
            print("Could not find book description")
            return None
        content_element = content_element.find_all("span")[1]        
    
    content = content_element.get_text()
    content = content.replace("An alternative cover edition for this ISBN can be found here.", "")
    return content.strip()

def get_num_pages(soup, is_beta=False):
    if is_beta:
        # New website format
        pages_element = soup.find("div", class_="FeaturedDetails")
    else:
        # Old website format
        pages_element = soup.find("span", itemprop="numberOfPages")

    try:
        num_pages_text = extract_element_text(pages_element)
    except AttributeError:
        logging.exception("Could not find number of book pages")
        return None
        
    return extract_integer(num_pages_text)

def get_num_ratings(soup, is_beta=False):
    if is_beta:
        # New website format
        num_ratings_element = soup.find("div", class_="RatingStatistics__meta").find_all("span")[0]
    else:
        # Old website format
        num_ratings_element = soup.find("a", href="#other_reviews")
    num_ratings_text = extract_element_text(num_ratings_element)
    return extract_integer(num_ratings_text)

def get_rating_value(soup, is_beta=False):
    if is_beta:
        return None
    else:
        # Old website format
        rating_value_element = soup.find("span", itemprop="ratingValue")
        rating_value_text = extract_element_text(rating_value_element)
        return rating_value_text 

def get_genres(soup, is_beta=False):
    if is_beta:
        return None
    else:
        # Old website format
        genres_list = soup.find("div", id="aboutAuthor").find_previous('div') # this doesnt work
        print(genres_list)



def get_book_metadata(link):
    is_beta = False
    response = requests.get(BASE_URL + link, headers=headers)
    print(BASE_URL + link)
    soup = bs(response.content, 'lxml')
    beta_button = soup.find("div", class_="BetaFeedbackButton")
    if beta_button is not None:
        is_beta = True
        print("Accessing beta website")
    
    metadata = {
        "title": get_title(soup, is_beta),
        "author":  get_author(soup, is_beta),
        "description": get_description(soup, is_beta),
        "num_pages": get_num_pages(soup, is_beta), # integer
        "num_ratings": get_num_ratings(soup, is_beta), # integer
        "rating_value": get_rating_value(soup, is_beta), # string
        "genres": get_genres(soup, is_beta)
    }
    return metadata




# book_links = get_book_links("/shelf/show/thriller")
# print(book_links)
# driver.get("https://www.goodreads.com/book/show/22557272-the-girl-on-the-train")
# print(driver)
print(get_book_metadata("/book/show/22557272-the-girl-on-the-train"))