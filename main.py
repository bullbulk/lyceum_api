import argparse
from io import BytesIO

from PIL import Image

from spn import *
from api_utils import *


class SearchError(BaseException):
    pass


parser = argparse.ArgumentParser()
parser.add_argument('name', type=str, nargs="*")

address_ll = ','.join(get_point(" ".join(parser.parse_args().name)))

search_api_server = "https://search-maps.yandex.ru/v1/"
org_api_key = "7bb93799-c0f9-45ee-8f5c-616a177a7cc3"

search_params = {
    "apikey": org_api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    print(response.json())
    raise SearchError

# Преобразуем ответ в json-объект
json_response = response.json()

# Получаем первую найденную организацию.
organization = json_response["features"][0]
# Название организации.
org_name = organization["properties"]["CompanyMetaData"]["name"]
# Адрес организации.
org_address = organization["properties"]["CompanyMetaData"]["address"]

# Получаем координаты ответа.
point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": address_ll,
    "spn": ",".join(map(str, get_spn(organization))),
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": "{0},pm2ntl".format(org_point)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)
with BytesIO(response.content) as buffer:
    Image.open(buffer).show()
