"""
Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для конкретного пользователя, сохранить JSON-вывод в файле *.json
"""
import requests

username = 'KonTroAl'

url = f'https://api.github.com/users/{username}/repos'

response = requests.get(url)
j_data = response.json()

print(f'All repositories of {username}: \n')
for item in j_data:
    print(item['name'])
