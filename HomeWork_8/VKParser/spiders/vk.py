import scrapy
from scrapy.http import HtmlResponse


class VkSpider(scrapy.Spider):
    name = 'vk'
    allowed_domains = ['vk.com']
    start_urls = ['https://vk.com/']
    vk_login_url = ''

    def parse(self, response: HtmlResponse):
        yield scrapy.FormRequest(
            self.vk_login_url,
            method='POST',
            callback=self.login,
            formdata={
                
            }
        )

    def login(self, response: HtmlResponse):
        print()