"""
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы (необходимо анализировать оба поля зарплаты).
Для тех, кто выполнил задание с Росконтролем - напишите запрос для поиска продуктов с рейтингом не ниже введенного или качеством не ниже введенного
(то есть цифра вводится одна, а запрос проверяет оба поля)
"""
from pymongo import MongoClient
from pprint import pprint

client = MongoClient('localhost', 27017)
db = client['vacancy_db']
vacancy_collection = db.vacancy

test_sum = 80000
currency = 'руб.'

vacancy_list = []

for doc in vacancy_collection.find({'currency': currency,
                                    '$or': [
                                        {'min_salary': {'$gte': test_sum}},
                                        {'max_salary': {'$gte': test_sum}}
                                    ]
                                    }):
    vacancy_list.append(doc)


pprint(vacancy_list)