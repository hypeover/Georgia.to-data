import requests
import json
import codecs
from tqdm import tqdm

data = []

data_request = requests.get('https://georgia.to/en/map-data/')
places = json.loads(data_request.text)

for place in tqdm(places, desc="Collecting places..."):
    place_request = requests.get(
        f"https://georgia.to/en/api/localized-detail/attraction/{place['id']}/"
    )

    if place_request.status_code != 200:
        continue

    place_details = json.loads(place_request.text)

    obj = {
        'placeid': place['id'],
        'lat': place['latitude'],
        'lon': place['longitude'],
        'thumbnail': place['thumbnail'],
        'url': place_details.get('url'),
        'types': place_details.get('types'),
        'title': codecs.decode(place_details.get('title', ''), 'unicode-escape'),
        'fav': False
    }

    data.append(obj)

with open('data.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print('Data has been successfully saved to data.json')
