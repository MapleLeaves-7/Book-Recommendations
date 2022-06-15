import scrapy
import re
import time
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
        self.is_beta = False

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options)

    def parse(self, response):
        # Let selenium load the page then pass html to scrapy
        self.driver.get(response.request.url)
        sel = scrapy.Selector(text=self.driver.page_source)

        # Check if it is the beta website
        beta_button = sel.xpath(
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
                    (By.CLASS_NAME, "content"))
            )
            time.sleep(0.6)

        sel = self.remove_old_modal(sel, response.request.url)

        yield {
            "title": self.get_title(sel),
            "author": self.get_author(sel),
            "description": self.get_description(sel),
            "num_pages": self.get_num_pages(sel),
            "num_ratings": self.get_num_ratings(sel),
            "rating_value": self.get_rating_value(sel),
            "genres": self.get_genres(sel)
        }

    # Check if modal window exists and reload until it is gone
    def remove_old_modal(self, sel, url):
        while True:
            old_modal_window = sel.xpath(
                '//*[contains(@class,"loginModal")]')

            if not old_modal_window:
                return sel

            self.driver.get(url)
            time.sleep(1)
            sel = scrapy.Selector(text=self.driver.page_source)

    def get_title(self, response):
        if self.is_beta:
            # New website format
            title = response.xpath(
                '//h1[@class="Text Text__title1"]/text()').get()
        else:
            # Old website format
            title = response.xpath('//h1[@id="bookTitle"]/text()').get()
        return title.strip()

    def get_author(self, response):
        if self.is_beta:
            # New website format
            return response.xpath('//span[@class="ContributorLink__name"]/text()').get()
        else:
            # Old website format
            return response.xpath('//a[@class="authorName"]/span/text()').get()

    def get_description(self, response):
        if self.is_beta:
            # New website format
            description = response.xpath(
                '//div[@class="BookPageMetadataSection__description"]//span[@class="Formatted"]/text()').get()
        else:
            # Old website format
            description = response.xpath(
                '//div[@id="description"]/span[2]/text()').get()

        description = description.replace(
            "An alternative cover edition for this ISBN can be found here.", "")
        return description.strip()

    def get_num_pages(self, response):
        if self.is_beta:
            num_pages_text = response.xpath(
                '//p[@data-testid="pagesFormat"]/text()').get()
        else:
            num_pages_text = response.xpath(
                '//span[@itemprop="numberOfPages"]/text()').get()
        return self.extract_integer(num_pages_text)

    def get_num_ratings(self, response):
        if self.is_beta:
            num_ratings_text = response.xpath(
                '//span[@data-testid="ratingsCount"][1]/text()').get()
        else:
            num_ratings_text = response.xpath(
                '//a[@href="#other_reviews"][1]/meta/@content').get()
        return self.extract_integer(num_ratings_text)

    def get_rating_value(self, response):
        if self.is_beta:
            rating_value = response.xpath(
                '//div[@class="RatingStatistics__rating"][1]/text()').get()
        else:
            rating_value = response.xpath(
                '//span[@itemprop="ratingValue"]/text()').get()
        return rating_value.strip()

    def get_genres(self, response):
        if self.is_beta:
            genre_sections = response.xpath(
                '//span[@class="BookPageMetadataSection__genre"]')
            print(genre_sections)
            genres = "nothing"
            print("haven't handled the beta yet")
        else:
            genre_anchor_tags = response.xpath(
                '//a[contains(@href, "/work/shelves/")]/../../following-sibling::div//div[contains(@class, "elementList ")]/div[@class="left"]//a')
            genres = {}
            for tag in genre_anchor_tags:
                link = tag.xpath('@href').get()
                name = tag.xpath('text()').get()
                genres[self.base_url + link] = name.lower()

        return genres

    def extract_integer(self, text):
        # Regex to extract number
        regex = re.compile("(?:(?:\d+),)*\d+")
        number_text = regex.search(text)
        if not number_text:
            print(text)
            print("Number extraction failed")
            return None
        number_text = number_text.group()
        number = number_text.replace(",", "")
        return int(number)
