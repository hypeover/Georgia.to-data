import requests
import json
import codecs

data = []

data_request = requests.get('https://georgia.to/en/map-data/')
places = json.loads(data_request.text)

for place in places:
    place_request = requests.get(f'https://georgia.to/en/api/localized-detail/attraction/{place['id']}/')
    if place_request.status_code != 200:
        continue
    place_details = json.loads(place_request.text)
    object = {
        'id': place['id'],
        'lat': place['latitude'],
        'lon': place['longitude'],
        'thumbnail': place['thumbnail'],
        'url': place_details['url'],
        'types': place_details['types'],
        'title': codecs.decode(place_details['title'], 'unicode-escape'),
        'fav': False
    }
    data.append(object)

with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)