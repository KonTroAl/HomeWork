from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

import settings
from HomeWork_8.VKParser.spiders.vk import VkSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(VkSpider)

    process.start()
