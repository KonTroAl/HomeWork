"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность)
с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:
- Наименование вакансии.
- Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
- Ссылку на саму вакансию.
- Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.
"""
import requests
from bs4 import BeautifulSoup

base_url = 'https://hh.ru'
# vacancy = input('Enter vacancy: ')
vacancy = 'Python'
url = 'https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&salary=&text=Python&from=suggest_post'

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.27 (Edition Yx 05)'}
params = {'text': vacancy.capitalize()}

response = requests.get(base_url + '/search/vacancy', headers=headers, params=params)
if response.ok:
    dom = BeautifulSoup(response.text, 'html.parser')
    result_list = []

    result = dom.findAll('div', {'class': 'vacancy-serp-item'})
    print(len(result))

