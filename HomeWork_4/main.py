"""
Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
- название источника;
- наименование новости;
- ссылку на новость;
- дата публикации.
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

news_links = []

news_pictures_links = dom_start.xpath("//div[contains(@class, 'daynews__item')]/a/@href")

for link in news_pictures_links:
    news_links.append(link)

