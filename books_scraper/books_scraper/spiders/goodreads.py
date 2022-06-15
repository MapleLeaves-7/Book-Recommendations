import scrapy
import re
import time
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class GoodreadsSpider(scrapy.Spider):
    name = "goodreads"
    start_urls = [
        "https://www.goodreads.com/book/show/22557272-the-girl-on-the-train"]

    def __init__(self):
        self.base_url = "https://www.goodreads.com"
        self.has_all_data = True

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options)

    def parse(self, response):
        self.has_all_data = True
        # Load page using selenium
        self.driver.get(response.request.url)
        # Set page selector to be the html of the page loaded into selenium
        page_sel = scrapy.Selector(text=self.driver.page_source)

        # Check if it is the beta website
        beta_button = page_sel.xpath(
            '//div[@class="BetaFeedbackButton"]')

        if beta_button:
            # Click out of the beta website
            while True:
                try:
                    # Find the beta button to click
                    self.driver.find_element_by_xpath(
                        '//span[contains(text(),"BETA")]/parent::button').click()

                    leave_beta_button = self.driver.find_element_by_xpath(
                        '//span[contains(text(),"Leave beta")]/parent::button')

                    # Try until the button loads
                    while not leave_beta_button:
                        time.sleep(0.6)
                        leave_beta_button = self.driver.find_element_by_xpath(
                            '//span[contains(text(),"Leave beta")]/parent::button')

                    time.sleep(1)
                    leave_beta_button.click()
                    break
                except:
                    # Reload the page if there is an overlay login window
                    self.driver.get(response.request.url)
                    time.sleep(0.6)

            # Wait until the old page has loaded or 30 seconds have passed
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//h1[@id="bookTitle"]'))
            )
            time.sleep(0.6)

            # Set the newly loaded old page as the selector element
            page_sel = scrapy.Selector(text=self.driver.page_source)

        # Reload page until login modal is gone for old page
        page_sel = self.remove_old_modal(page_sel, response.request.url)

        try:
            yield {
                "has_all_data": self.has_all_data,
                "title": self.get_title(page_sel),
                "author": self.get_author(page_sel),
                "description": self.get_description(page_sel),
                "num_pages": self.get_num_pages(page_sel),
                "num_ratings": self.get_num_ratings(page_sel),
                "rating_value": self.get_rating_value(page_sel),
                "genres": self.get_genres(page_sel, response.request.url),
                "settings": self.get_settings(page_sel, response.request.url),
                "date_published": self.get_date_published(page_sel)
            }
        except:
            yield {
                "has_all_data": False,
                "title": None,
                "author": None,
                "description": None,
                "num_pages": None,
                "num_ratings": None,
                "rating_value": None,
                "genres": None
            }

    # Check if modal window exists and reload until it is gone
    def remove_old_modal(self, page_sel, url):
        while True:
            old_modal_window = page_sel.xpath(
                '//*[contains(@class,"loginModal")]')

            if not old_modal_window:
                return page_sel

            self.driver.get(url)
            time.sleep(1)
            page_sel = scrapy.Selector(text=self.driver.page_source)

    def get_title(self, page_sel):
        title = page_sel.xpath('//h1[@id="bookTitle"]/text()').get()
        return title.strip()

    def get_author(self, page_sel):
        author = page_sel.xpath('//a[@class="authorName"]/span/text()').get()
        return author.strip()

    def get_description(self, page_sel):
        description = page_sel.xpath(
            '//div[@id="description"]/span[2]/text()').get()

        description = description.replace(
            "An alternative cover edition for this ISBN can be found here.", "")
        return description.strip()

    def get_num_pages(self, page_sel):
        num_pages_text = page_sel.xpath(
            '//span[@itemprop="numberOfPages"]/text()').get()
        return self.extract_integer(num_pages_text)

    def get_num_ratings(self, page_sel):
        num_ratings_text = page_sel.xpath(
            '//a[@href="#other_reviews"][1]/meta/@content').get()
        return self.extract_integer(num_ratings_text)

    def get_rating_value(self, page_sel):
        rating_value = page_sel.xpath(
            '//span[@itemprop="ratingValue"]/text()').get()
        return rating_value.strip()

    def get_genres(self, page_sel, url):
        genre_anchor_tags = page_sel.xpath(
            '//a[contains(@href, "/work/shelves/")]/../../following-sibling::div//div[contains(@class, "elementList ")]/div[@class="left"]//a')
        return self.extract_link_and_name(genre_anchor_tags, url)

    def get_settings(self, page_sel, url):
        setting_anchor_tags = page_sel.xpath('//a[contains(@href,"/places")]')
        return self.extract_link_and_name(setting_anchor_tags, url)

    def get_date_published(self, page_sel):
        date_published = page_sel.xpath(
            '//div[contains(text(), "Published")]/text()').get()

        # Remove multiple spaces and newlines
        date_published = " ".join(date_published.split())

        date_regex = re.compile(
            '(?P<month>\w+)\s(?P<day>\d{1,2})(?:st|nd|rd|th)\s(?P<year>\d{4})')
        match = date_regex.search(date_published)

        try:
            return {
                "day": match.group('day'),
                "month": match.group('month').lower(),
                "year": match.group('year')
            }
        except AttributeError:
            # Did not find a match for the date
            self.has_all_data = False
            return None

    def extract_link_and_name(self, anchor_tags, url):
        link_and_name = {}
        for tag in anchor_tags:
            link = tag.xpath('@href').get()
            name = tag.xpath('text()').get()
            link_and_name[urljoin(url, link)] = name.lower()

        return link_and_name

    def extract_integer(self, text):
        # Regex to extract number
        regex = re.compile("(?:(?:\d+),)*\d+")
        number_text = regex.search(text)
        if not number_text:
            print(text)
            print("Number extraction failed")
            self.has_all_data = False
            return None
        number_text = number_text.group()
        number = number_text.replace(",", "")
        return int(number)
