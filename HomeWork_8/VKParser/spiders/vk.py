import scrapy


class VkSpider(scrapy.Spider):
    name = 'vk'
    allowed_domains = ['vk.com']
    start_urls = ['https://vk.com/']

    def parse(self, response):
        pass
