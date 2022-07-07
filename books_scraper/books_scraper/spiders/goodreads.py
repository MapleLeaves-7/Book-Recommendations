import scrapy
import time
import re
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.loader import ItemLoader
from books_scraper.items import BookMetadataItem, remove_extra_spaces


class GoodreadsSpider(scrapy.Spider):
    name = "goodreads"

    def __init__(self):
        self.base_url = "https://www.goodreads.com"

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options)

    def start_requests(self):
        # start_urls = ["https://www.goodreads.com/shelf/show/thriller"]
        # start_urls = ["https://www.goodreads.com/book/show/22557272-the-girl-on-the-train"]
        # start_urls = ["https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once"]
        start_urls = ["https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page=6"]
        # start_urls = ["https://www.goodreads.com/book/show/264196.1984"]

        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse_list)
            # yield scrapy.Request(url=url, callback=self.parse_book_metadata)

    def parse_list(self, response):
        book_links = response.xpath('//a[@class="bookTitle"]/@href').extract()

        # save book links crawled from page list into db first
        for link in book_links:
            loader = ItemLoader(item=BookMetadataItem(), selector=response)
            loader.add_value('link', urljoin(response.request.url, link))
            attributes = ["title", "authors", "description", "num_pages", "num_ratings", "rating_value",
                          "date_published", "book_cover", "language", "genres", "date_published", "related_book_links"]
            for attribute in attributes:
                loader.add_value(attribute, None)

            metadata_item = loader.load_item()
            yield metadata_item

        # crawl into book link to get metadata
        for link in book_links:
            time.sleep(2)
            yield scrapy.Request(url=response.urljoin(link), callback=self.parse_book_metadata)

        # i = 0
        # for link in book_links:
        #     if i > 2:
        #         break
        #     yield scrapy.Request(url=response.urljoin(link), callback=self.parse_book_metadata)
        #     i += 1

        next_page_disabled = response.xpath('//span[@class="next_page disabled"]')
        if not next_page_disabled:
            page_number_regex = re.compile('\?page=(\d{1,3})')
            match = page_number_regex.search(response.url)
            if match:
                next_page = int(match.group(1)) + 1
                next_page_url = re.sub(r"\?page=\d{1,3}", f"?page={next_page}", response.url)
            else:
                next_page_url = response.url + "?page=2"

            yield response.follow(url=next_page_url, callback=self.parse_list)

    def parse_book_metadata(self, response):
        # Load page using selenium
        self.driver.get(response.request.url)
        # Set page selector to be the html of the page loaded into selenium
        page_sel = scrapy.Selector(text=self.driver.page_source)

        # Check if it is the beta website
        beta_button = page_sel.xpath('//div[@class="BetaFeedbackButton"]')

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

        related_book_links = self.get_related_book_links(page_sel)

        try:
            loader.add_value('link', response.request.url)
            loader.add_xpath('title', '//h1[@id="bookTitle"]/text()')
            loader.add_value('authors', self.get_authors(page_sel, response.request.url))
            loader.add_value('description', self.get_description(page_sel))
            loader.add_xpath('num_pages', '//span[@itemprop="numberOfPages"]/text()')
            loader.add_xpath('num_ratings', '//a[@href="#other_reviews"][1]/meta/@content')
            loader.add_xpath('rating_value', '//span[@itemprop="ratingValue"]/text()')
            loader.add_xpath('date_published', '//div[contains(text(), "Published")]/text()')
            loader.add_xpath('book_cover', '//img[@id="coverImage"]/@src')
            loader.add_xpath('language', '//div[@itemprop="inLanguage"]/text()')
            loader.add_value('genres', self.get_genres(page_sel, response.request.url))
            loader.add_value('settings', self.get_settings(page_sel, response.request.url))
            # loader.add_xpath('related_book_links', '//h2[contains(text(),"also enjoyed")]/../..//a[contains(@href,"book/show/")]/@href')
            loader.add_value('related_book_links', related_book_links)

            metadata_item = loader.load_item()
            yield metadata_item
        except Exception as e:
            print(e)
            loader.add_value('link', response.request.url)
            attributes = ["title", "authors", "description", "num_pages", "num_ratings", "rating_value",
                          "date_published", "book_cover", "language", "genres", "date_published", "related_book_links"]
            for attribute in attributes:
                loader.add_value(attribute, None)

            metadata_item = loader.load_item()
            yield metadata_item

        # print(related_book_links)
        # for link in related_book_links:
        #     if link:
        #         time.sleep(2)
        #         yield response.follow(response.urljoin(link), callback=self.parse_book_metadata)

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

    def get_authors(self, page_sel, url):
        author_anchor_tags = page_sel.xpath('//a[@class="authorName"]')
        return self.extract_link_and_name(author_anchor_tags, url, extract_author=True)

    def get_description(self, page_sel):
        # try to extract longer paragraph first
        description = page_sel.xpath('//div[@id="description"]/span[2]/text()').extract()

        # extract shorter paragraph if longer paragraph does not exist
        if not description:
            description = page_sel.xpath('//div[@id="description"]/span/text()').extract()

        return description

    def get_genres(self, page_sel, url):
        genre_anchor_tags = page_sel.xpath(
            '//a[contains(@href, "/work/shelves/")]/../../following-sibling::div//div[contains(@class, "elementList ")]/div[@class="left"]//a')
        return self.extract_link_and_name(genre_anchor_tags, url)

    def get_settings(self, page_sel, url):
        setting_anchor_tags = page_sel.xpath('//a[contains(@href,"/places")]')
        return self.extract_link_and_name(setting_anchor_tags, url)

    def get_related_book_links(self, page_sel):
        return page_sel.xpath('//h2[contains(text(),"also enjoyed")]/../..//a[contains(@href,"book/show/")]/@href').extract()

    def extract_link_and_name(self, anchor_tags, url, extract_author=False):
        link_and_name = {}
        for tag in anchor_tags:
            link = tag.xpath('@href').get()
            if extract_author:
                name = tag.xpath('./span/text()').get()
            else:
                name = tag.xpath('text()').get()
            link_and_name[urljoin(url, link)] = remove_extra_spaces(name.lower())

        # if there was no data extracted, return None
        if not link_and_name:
            return None
        return link_and_name
