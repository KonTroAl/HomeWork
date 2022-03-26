import scrapy
from scrapy.http import HtmlResponse


class VkSpider(scrapy.Spider):
    name = 'vk'
    allowed_domains = ['vk.com']
    start_urls = ['https://vk.com/']
    vk_login_url = 'https://login.vk.com/?act=web_token'
    access_token = '993d38d9f1ddfb31b183289699eb8bac6dca1b437895886bb7af88c22684b54bf6cf0a8aa76097901d9ef'
    app_id = '6287487'

    link = 'https://oauth.vk.com/authorize?client_id=8116057&display=page&redirect_uri=http://example.com/callback&scope=friends&response_type=token&v=5.131&state=123456'

    def parse(self, response: HtmlResponse):
        yield scrapy.FormRequest(
            self.vk_login_url,
            method='POST',
            callback=self.login,
            formdata={
                'app_id': self.app_id,
                'access_token': self.access_token
            }
        )

    def login(self, response: HtmlResponse):
        print()