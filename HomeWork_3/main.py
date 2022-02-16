"""
Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем должность)
с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
Получившийся список должен содержать в себе минимум:
+ Наименование вакансии.
+ Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. Цифры преобразуем к цифрам).
+ Ссылку на саму вакансию.
- Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
Структура должна быть одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в json либо csv.
"""
import requests
from bs4 import BeautifulSoup
from pprint import pprint
import json

base_url = 'https://hh.ru'
# vacancy = input('Enter vacancy: ')
vacancy = 'Python'
url_f = 'https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&salary=&text=Python&from=suggest_post'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.27 (Edition Yx 05)'}

params = {'text': vacancy.capitalize(), 'page': 0}
result_list = []
while True:
    response = requests.get(base_url + '/search/vacancy', headers=headers, params=params)
    if response.ok:
        dom = BeautifulSoup(response.text, 'html.parser')

        result = dom.findAll('div', {'class': 'vacancy-serp-item'})

        for item in result:
            result_data = {}
            vacancy_name = item.find('a').getText()
            result_data['vacancy_name'] = vacancy_name

            vacancy_link = base_url + item.find('a')['href']
            result_data['vacancy_link'] = vacancy_link

            vacancy_salary = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
            if vacancy_salary:
                salary = vacancy_salary.getText()
                salary_list = salary.split()
                currency = salary_list[-1]
                result_data['currency'] = currency
                try:
                    min_salary = int(salary_list[0] + salary_list[1])
                except ValueError:
                    min_salary = int(salary_list[1] + salary_list[2])

                result_data['min_salary'] = min_salary
                if len(salary_list) > 4:
                    try:
                        max_salary = int(salary_list[3] + salary_list[4])
                    except ValueError:
                        max_salary = int(salary_list[2] + salary_list[3])
                    result_data['max_salary'] = max_salary
            result_data['site'] = 'HeadHunter'
            result_list.append(result_data)

        next_page_div = dom.find('div', {'class': 'pager'})
        next_page = next_page_div.find(text='дальше')
        if next_page:
            params['page'] += 1
        else:
            break
    else:
        break

with open('result.json', 'w') as file:
    json.dump(result_list, file, indent=4)
