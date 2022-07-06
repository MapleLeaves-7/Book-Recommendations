import re
import datetime
from scrapy.item import Item, Field
from itemloaders.processors import MapCompose, TakeFirst, Join


# Remove mutiple spaces and newlines
def remove_extra_spaces(text):
    return " ".join(text.split())


def clean_description(text):
    return text.replace("An alternative cover edition for this ISBN can be found here.", "")


# Check that text contains words
def word_exists(text):
    regex = re.compile("(?:\w+\s)*\w+")
    match = regex.search(text)
    if not match:
        return None
    return match.group()


def extract_integer(text):
    # Regex to extract number
    regex = re.compile("(?:(?:\d+),)*\d+")
    match = regex.search(text)
    if not match:
        return None
    number_text = match.group()
    number = number_text.replace(",", "")
    return int(number)


def extract_float(text):
    # Regex to extract float
    regex = re.compile("^[0-5](?:\.\d{1,2})?")
    match = regex.search(text)
    if not match:
        return None
    return float(match.group())


def extract_date(date_published):
    date_regex = re.compile(
        '(?P<month>\w+)\s(?P<day>\d{1,2})(?:st|nd|rd|th)\s(?P<year>\d{4})')
    match = date_regex.search(date_published)

    try:
        day = match.group('day')
        month = match.group('month').capitalize()
        year = match.group('year')
        formatted_date = f"{day} {month} {year}"

        datetime_object = datetime.datetime.strptime(
            formatted_date, "%d %B %Y")

        date_object = datetime_object.date()
        return date_object
    except AttributeError:
        # Did not find a match for the date
        return None


class BookMetadataItem(Item):
    link = Field(output_processor=TakeFirst())
    title = Field(input_processor=MapCompose(word_exists, remove_extra_spaces), output_processor=TakeFirst())
    authors = Field(output_processor=TakeFirst())
    description = Field(input_processor=MapCompose(word_exists, clean_description, remove_extra_spaces), output_processor=Join())
    num_pages = Field(input_processor=MapCompose(extract_integer), output_processor=TakeFirst())
    num_ratings = Field(input_processor=MapCompose(extract_integer), output_processor=TakeFirst())
    rating_value = Field(input_processor=MapCompose(remove_extra_spaces, extract_float), output_processor=TakeFirst())
    genres = Field(output_processor=TakeFirst())
    settings = Field(output_processor=TakeFirst())
    date_published = Field(input_processor=MapCompose(remove_extra_spaces, extract_date), output_processor=TakeFirst())
    related_book_links = Field()
