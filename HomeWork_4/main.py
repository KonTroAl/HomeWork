"""
Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
+ название источника;
- наименование новости;
+ ссылку на новость;
+ дата публикации.
Сложить собранные новости в БД
Минимум один сайт, максимум - все три
"""

import requests
from pprint import pprint
import json
from lxml import html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

url = 'https://news.mail.ru'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.27 (Edition Yx 05)'}

start_response = requests.get(url, headers=headers)

dom_start = html.fromstring(start_response.text)


def get_links():
    news_links = []
    news_pictures_links = dom_start.xpath("//div[contains(@class, 'daynews__item')]//a/@href")

    for link in news_pictures_links:
        news_link = link.split('.')
        if 'https://sportmail' in news_link:
            pass
        else:
            news_links.append(link)

    news_ul_links = dom_start.xpath("//div[@class='js-module']/ul/li[@class='list__item']//a/@href")

    for link in news_ul_links:
        news_link = link.split('.')
        if 'https://sportmail' in news_link:
            pass
        else:
            news_links.append(link)

    return news_links


links_list = get_links()

news_list = []

for link in links_list:
    news_dict = {}
    news_dict['news_link'] = link

    new_response = requests.get(link, headers=headers)
    new_dom = html.fromstring(new_response.text)

    date_source_items = new_dom.xpath("//span[@class='breadcrumbs__item']")
    for item in date_source_items:
        date = item.xpath("//span[@class='breadcrumbs__item']//span[@datetime]/@datetime")[0]
        source = item.xpath("//span[@class='breadcrumbs__item']//span[@class='link__text']/text()")[0]
        news_dict['date'] = date
        news_dict['source'] = source

    title = new_dom.xpath("//div[contains(@class, 'hdr_collapse')]//h1[@class='hdr__inner']/text()")[0]
    news_dict['title'] = title

    news_list.append(news_dict)

pprint(news_list)
