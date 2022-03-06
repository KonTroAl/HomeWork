import scrapy
from scrapy.http import HtmlResponse


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
        name = response.xpath("//h1/text()").get()
        price = response.xpath("//span[@slot='price']/text()").get()
        currency = response.xpath("//span[@slot='currency']/text()").get()
        link = response.url
        
