from bs4 import BeautifulSoup as bs
import requests
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

# def get_book_links(link):
#     response = requests.get(BASE_URL + link)
#     soup = bs(response.content, "lxml")
#     books = soup.find_all("a", class_="bookTitle")
#     book_links = [b['href'] for b in books]
#     return book_links

def get_element_text(element):
    text = element.get_text()
    return text.strip()

def get_title(soup):
     # Format for old website
    title_element = soup.find("h1", id="bookTitle")
    
    if title_element is None:
        # Format for new beta website
        title_element = soup.find("h1", class_="Text Text__title1")
       
    return get_element_text(title_element)

def get_author(soup):
   # Format for old website
    author_element = soup.find("a", class_="authorName")
    author_element = author_element.find("span")
    if author_element is None:
         # Format for new beta website
        author_element = soup.find("span", class_="ContributorLink__name")
        
    return get_element_text(author_element)

def get_description(soup):
    # print(soup.prettify())
    # Format for old website
    content_element = soup.find("div", id="description").find_all("span")[1]
    if content_element is None:
        # Format for new website
        content_element = soup.find("div", class_="BookPageMetadataSection__description").find("span", class_="Formatted")
    
    content = content_element.get_text()
    content = content.replace("An alternative cover edition for this ISBN can be found here.", "")
    return content.strip()


def get_book_metadata(link):
    metadata = {}
    response = requests.get(BASE_URL + link)
    print(BASE_URL + link)
    soup = bs(response.content, 'lxml')
    metadata = {
        "title": get_title(soup),
        "author":  get_author(soup),
        "description": get_description(soup),
    }
    return metadata




# book_links = get_book_links("/shelf/show/thriller")
# print(book_links)
# driver.get("https://www.goodreads.com/book/show/22557272-the-girl-on-the-train")
# print(driver)
print(get_book_metadata("/book/show/22557272-the-girl-on-the-train"))