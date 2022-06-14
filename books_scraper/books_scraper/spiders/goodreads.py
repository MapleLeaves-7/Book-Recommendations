import scrapy
import re


class GoodreadsSpider(scrapy.Spider):
    name = "goodreads"
    start_urls = [
        "https://www.goodreads.com/book/show/22557272-the-girl-on-the-train"]

    def parse(self, response):
        beta_button = response.xpath('//div[@class="BetaFeedbackButton"]')
        if beta_button:
            is_beta = True
            print("Accessing the beta website")
        else:
            print("Accessing the regular website")
            is_beta = False

        yield {
            "title": self.get_title(response, is_beta),
            "author": self.get_author(response, is_beta),
            "description": self.get_description(response, is_beta),
            "num_pages": self.get_num_pages(response, is_beta),
            "num_ratings": self.get_num_ratings(response, is_beta),
            "rating_value": self.get_rating_value(response, is_beta),
            "genres": self.get_genres(response, is_beta)
        }

    def get_title(self, response, is_beta):
        if is_beta:
            # New website format
            title = response.xpath(
                '//h1[@class="Text Text__title1"]/text()').get()
        else:
            # Old website format
            title = response.xpath('//h1[@id="bookTitle"]/text()').get()
        return title.strip()

    def get_author(self, response, is_beta):
        if is_beta:
            # New website format
            return response.xpath('//span[@class="ContributorLink__name"]/text()').get()
        else:
            # Old website format
            return response.xpath('//a[@class="authorName"]/span/text()').get()

    def get_description(self, response, is_beta):
        if is_beta:
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

    def get_num_pages(self, response, is_beta):
        if is_beta:
            num_pages_text = response.xpath(
                '//p[@data-testid="pagesFormat"]/text()').get()
        else:
            num_pages_text = response.xpath(
                '//span[@itemprop="numberOfPages"]/text()').get()
        return self.extract_integer(num_pages_text)

    def get_num_ratings(self, response, is_beta):
        if is_beta:
            num_ratings_text = response.xpath(
                '//span[@data-testid="ratingsCount"][1]/text()').get()
        else:
            num_ratings_text = response.xpath(
                '//a[@href="#other_reviews"][1]/meta/@content').get()
        return self.extract_integer(num_ratings_text)

    def get_rating_value(self, response, is_beta):
        if is_beta:
            rating_value = response.xpath(
                '//div[@class="RatingStatistics__rating"][1]/text()').get()
        else:
            rating_value = response.xpath(
                '//span[@itemprop="ratingValue"]/text()').get()
        return rating_value.strip()

    def get_genres(self, response, is_beta):
        if is_beta:
            print("haven't handled the beta yet")
        else:
            genre_anchor_tags = response.xpath(
                '//a[contains(@href, "/work/shelves/")]/../../following-sibling::div//div[contains(@class, "elementList ")]/div[@class="left"]//a')
            genres = {}
            for tag in genre_anchor_tags:
                link = tag.xpath('@href').get()
                name = tag.xpath('text()').get()
                genres[link] = name.lower()

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
