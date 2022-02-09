"""
Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
"""

import requests

key = '260c4fkz3WOoLJRUCOvC8ocum1uKF3AaE6eHoPEA71F0BHiwRGw4GVoK'

artist = 'Linkin Park'

artist_url = f'https://api.happi.dev/v1/music?q={artist}&limit=&apikey={key}'

response_artist = requests.get(artist_url)
j_data_artist = response_artist.json()

artist_result = j_data_artist['result']
id_artist = artist_result[0]['id_artist']

album_url = f"https://api.happi.dev/v1/music/artists/{id_artist}/albums?apikey={key}"

response_album = requests.get(album_url)
j_data_album = response_album.json()

album_result = j_data_album['result']

album_dict = album_result['albums']

for item in album_dict:
    print(item['album'])
