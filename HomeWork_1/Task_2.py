"""
Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
"""

"""Скрипт для поиска всех альбомов определенного артиста. API = https://happi.dev/ """
import requests
from .key import KEY


"""Имя артиста для поиска альбома"""
ARTIST = 'Linkin Park'

artist_url = f'https://api.happi.dev/v1/music?q={ARTIST}&limit=&apikey={KEY}'
j_data_artist = requests.get(artist_url).json()
artist_result = j_data_artist['result']

"""id артиста необходимо для поиска альбома"""
id_artist = artist_result[0]['id_artist']

"""Поиск альбома"""
album_url = f"https://api.happi.dev/v1/music/artists/{id_artist}/albums?apikey={KEY}"
j_data_album = requests.get(album_url).json()
album_dict = j_data_album['result']['albums']

print(f'All albums of {ARTIST}: \n')
for item in album_dict:
    print(item['album'])
