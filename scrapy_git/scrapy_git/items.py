from datetime import datetime

from itemloaders.processors import TakeFirst, MapCompose, Join
from scrapy import Field, Item


def datetime_response(value):
    need_date = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ")
    return need_date


def del_html(value):
    return value.strip()

def encod_string(value):
    value.encode('utf-8')


def digit_some(value):
    if 'k' in value:
        value = value.replace('k', '').replace('.', '')
        print(value)
        return int(value)*100
    if ',' in value:
        value = value.replace(',', '')
        return int(value)
    return int(value)


def get_unicode_string(value):
    return value.encode('utf-8')


class ScrapyLastCommit(Item):
    author = Field(output_processor=TakeFirst())
    name = Field(input_processor=MapCompose(del_html), output_processor=TakeFirst())
    datetime_UTC = Field(input_processor=MapCompose(del_html, datetime_response), output_processor=TakeFirst())


class ScrapyLastRelease(Item):
    version = Field(input_processor=MapCompose(del_html), output_processor=TakeFirst())
    datetime_UTC = Field(input_processor=MapCompose(del_html, datetime_response), output_processor=TakeFirst())
    changelog = Field(output_processor=Join())


class ScrapyGitItem(Item):
    name = Field(input_processor=MapCompose(del_html), output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    about = Field(input_processor=MapCompose(del_html), output_processor=Join())
    site = Field(output_processor=TakeFirst())
    count_stars = Field(input_processor=MapCompose(digit_some), output_processor=TakeFirst())
    count_forks = Field(input_processor=MapCompose(digit_some), output_processor=TakeFirst())
    count_watching = Field(input_processor=MapCompose(digit_some), output_processor=TakeFirst())
    count_commit = Field(input_processor=MapCompose(digit_some), output_processor=TakeFirst())
    info_last_commit = Field(output_processor=TakeFirst())
    count_release = Field(input_processor=MapCompose(digit_some), output_processor=TakeFirst())
    info_last_release = Field(output_processor=TakeFirst())
