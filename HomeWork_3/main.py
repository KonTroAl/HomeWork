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


def search_currency():
    currency = {}
    key = 1
    for doc in vacancy_collection.find({}):
        try:
            if doc['currency'] in currency.values():
                pass
            else:
                currency[key] = doc['currency']
                key += 1
        except KeyError:
            pass
    return currency


def search_vacancy(currency_dict):
    vacancy_list = []
    currency_key = int(input('Choose currency. Enter number of currency (1: "USD", 2: "грн.", 3: "руб.", 4: "KZT", 5: "EUR"): '))
    currency = currency_dict[currency_key]
    test_sum = int(input('Enter salary: '))

    for doc in vacancy_collection.find({'currency': currency,
                                        '$or': [
                                            {'min_salary': {'$gte': test_sum}},
                                            {'max_salary': {'$gte': test_sum}}
                                        ]
                                        }):
        vacancy_list.append(doc)

    print(f'Общее количество вакансий по заданным параметрам {vacancy_list}')
    return vacancy_list


currency_dict = search_currency()
pprint(search_vacancy(currency_dict))

