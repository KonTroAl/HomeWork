# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, Compose,TakeFirst

def int_price(price):
    try:
        result = price[0].replace(' ', '')
        return int(result)
    except:
        return price


class LeroymerlinparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=Compose(int_price))
    currency = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field()
    photos = scrapy.Field()
    _id = scrapy.Field()

