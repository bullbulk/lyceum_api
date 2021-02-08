import requests

geocoder_api_key = "40d1649f-0493-4b70-98ba-98533de7710b"
geocoder_server = 'https://geocode-maps.yandex.ru/1.x/'


def fetch_data(geocodes_):
    res = []

    for geocode in geocodes_:
        params = {
            'apikey': geocoder_api_key,
            'geocode': geocode,
            'format': 'json',
            'results': 1
        }

        res.append(
            requests.get(geocoder_server, params=params).json()
            ['response']['GeoObjectCollection']['featureMember'][0]['GeoObject'])

    return res


def get_point(address: str) -> list:
    geocoder_object = fetch_data([address])
    point = geocoder_object[0]['Point']['pos']
    return point.split()
