import requests
from Request.parameters import add_parameters

# Константы состояний
Q, CITY, SEX, AGE_FROM, AGE_TO, STATUS, COUNT = range(7)

VK_TOKEN = '1111111111111111111111111111111111111111111111111111111111111111111111111111111111111'
VERSION = 5.89

button_help = "Help"


# Запрос для поиска людей по заданным критериям через VK API
def vk_request(content):
    url = 'https://api.vk.com/method/users.search'
    search_parameters = {
        'access_token': VK_TOKEN,
        'v': VERSION,
        'sort': '0',
        'fields': 'bdate, city',
    }
    add_parameters(content, search_parameters)
    response = requests.get(url, params=search_parameters)
    return response


# Получение фотографии с аватарки пользователя
def photo_request(content):
    photo_url = 'https://api.vk.com/method/photos.get'
    photo_parameters = {
        'owner_id': content["id"],
        'access_token': VK_TOKEN,
        'album_id': "profile",
        'v': 5.122,
    }
    photo_response = requests.get(photo_url, params=photo_parameters)
    return photo_response
