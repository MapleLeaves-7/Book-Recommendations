import scrapy
import time
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.loader import ItemLoader
from books_scraper.items import BookMetadataItem


class GoodreadsSpider(scrapy.Spider):
    name = "goodreads"

    def __init__(self):
        self.base_url = "https://www.goodreads.com"

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        # options.add_argument('--headless')
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options)

    def start_requests(self):
        # start_urls = ["https://www.goodreads.com/shelf/show/thriller"]
        start_urls = ["https://www.goodreads.com/book/show/22557272-the-girl-on-the-train"]

        for url in start_urls:
            # yield scrapy.Request(url=url, callback=self.parse_shelves)
            yield scrapy.Request(url=url, callback=self.parse_book_metadata)

    # def parse_shelves(self, response):
    #     book_links = response.xpath('//a[@class="bookTitle"]/@href').extract()
    #     # for link in book_links:
    #     #     yield scrapy.Request(url=response.urljoin(link), callback=self.parse_book_metadata)
    #     i = 0
    #     for link in book_links:
    #         if i > 2:
    #             break
    #         yield scrapy.Request(url=response.urljoin(link), callback=self.parse_book_metadata)
    #         i += 1

    def parse_book_metadata(self, response):
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

        loader = ItemLoader(item=BookMetadataItem(), selector=page_sel)

        try:
            loader.add_value('link', response.request.url)
            loader.add_xpath('title', '//h1[@id="bookTitle"]/text()')
            loader.add_xpath('author', '//a[@class="authorName"]/span/text()')
            loader.add_xpath('description', '//div[@id="description"]/span[2]/text()')
            loader.add_xpath('num_pages', '//span[@itemprop="numberOfPages"]/text()')
            loader.add_xpath('num_ratings', '//a[@href="#other_reviews"][1]/meta/@content')
            loader.add_xpath('rating_value', '//span[@itemprop="ratingValue"]/text()')
            loader.add_value('genres', self.get_genres(page_sel, response.request.url))
            loader.add_value('settings', self.get_settings(page_sel, response.request.url))
            loader.add_xpath('date_published', '//div[contains(text(), "Published")]/text()')
            loader.add_xpath('related_books', '//h2[contains(text(),"also enjoyed")]/../..//a[contains(@href,"book/show/")]/@href')

            metadata_item = loader.load_item()
            yield metadata_item 
        except:
            loader.add_value('link', response.request.url)
            attributes = ["title", "author", "description", "num_pages", "num_ratings", "rating_value", "date_published", "genres", "date_published", "related_books"]
            for attribute in attributes:
                loader.add_value(attribute, None)
            
            metadata_item = loader.load_item()
            yield metadata_item

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

    def get_genres(self, page_sel, url):
        genre_anchor_tags = page_sel.xpath(
            '//a[contains(@href, "/work/shelves/")]/../../following-sibling::div//div[contains(@class, "elementList ")]/div[@class="left"]//a')
        return self.extract_link_and_name(genre_anchor_tags, url)

    def get_settings(self, page_sel, url):
        setting_anchor_tags = page_sel.xpath('//a[contains(@href,"/places")]')
        return self.extract_link_and_name(setting_anchor_tags, url)

    def extract_link_and_name(self, anchor_tags, url):
        link_and_name = {}
        for tag in anchor_tags:
            link = tag.xpath('@href').get()
            name = tag.xpath('text()').get()
            link_and_name[urljoin(url, link)] = name.lower()

        # if there was no data extracted, return None
        if not link_and_name:
            return None
        return link_and_name
