"""
1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, которая будет добавлять только новые вакансии/продукты в вашу базу.

"""
import requests
import json
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

client = MongoClient('localhost', 27017)
db = client['vacancy_db']
vacancy_collection = db.vacancy

base_url = 'https://hh.ru'
# vacancy = input('Enter vacancy: ')
vacancy = 'Python'
url_f = 'https://hh.ru/search/vacancy?clusters=true&ored_clusters=true&enable_snippets=true&salary=&text=Python&from=suggest_post'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36 OPR/83.0.4254.27 (Edition Yx 05)'}

params = {'text': vacancy.capitalize(), 'page': 0, 'items_on_page': 20}
result_list = []
start_id = 0
count_of_new_vacancy = 0
while True:
    response = requests.get(base_url + '/search/vacancy', headers=headers, params=params)
    if response.ok:
        dom = BeautifulSoup(response.text, 'html.parser')

        result = dom.findAll('div', {'class': 'vacancy-serp-item'})

        for item in result:
            result_data = {}
            result_data['_id'] = start_id
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
                new_salary = salary.strip().replace('\u202f', '').replace('-', '').split()
                try:
                    min_salary = int(new_salary[0])
                except ValueError:
                    min_salary = int(new_salary[1])
                result_data['min_salary'] = min_salary
                if len(new_salary) > 4:
                    try:
                        max_salary = int(new_salary[3])
                    except ValueError:
                        max_salary = int(new_salary[2])

                    result_data['max_salary'] = max_salary

            result_data['site'] = 'HeadHunter'
            result_list.append(result_data)
            start_id += 1

            try:
                db_list = []

                db_dict = vacancy_collection.find({})

                if db_dict:
                    for doc in db_dict:
                        db_list.append(doc['vacancy_link'])

                    last_id = len(db_list)

                    if result_data['vacancy_link'] in db_list:
                        for item in vacancy_collection.find({'vacancy_link': result_data['vacancy_link']}):
                            result_data['_id'] = item['_id']
                            vacancy_collection.update_one({'_id': item['_id']}, {'$set': result_data})
                    else:
                        result_data['_id'] = last_id
                        vacancy_collection.insert_one(result_data)
                        count_of_new_vacancy += 1
                else:
                    vacancy_collection.insert_one(result_data)
                    count_of_new_vacancy += 1
            except dke:
                pass

        next_page_div = dom.find('div', {'class': 'pager'})
        next_page = next_page_div.find(text='дальше')
        if next_page:
            params['page'] += 1
        else:
            print(f'в базу данных добавлено новых вакансий: {count_of_new_vacancy}')
            break
    else:
        break
