import scrapy
from scrapy.http import HtmlResponse
from HomeWork_7.LeroyMerlinParser.items import LeroymerlinparserItem
from scrapy.loader import ItemLoader



class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, **kwargs):
        super(LeroymerlinSpider, self).__init__(**kwargs)
        self.start_urls =[f'https://leroymerlin.ru/search/?q={kwargs.get("search")}/']


    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@data-qa='product-name']")
        for link in links:
            yield response.follow(link, callback=self.parse_data)

    def parse_data(self, response: HtmlResponse):
        print()
        loader = ItemLoader(item=LeroymerlinparserItem(), response=response)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('price', "//span[@slot='price']/text()")
        loader.add_xpath('currency', "//span[@slot='currency']/text()")
        loader.add_value('link', response.url)
        loader.add_xpath('photos', '//picture[@slot="pictures"]/source[contains(@media, "1024px")]/@srcset')
        yield loader.load_item()


