import json
import logging
import requests

Vk_json_dict = {}


class VkPhoto:
    logging.basicConfig(filename='logging_file.log', filemode='w', level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    def __init__(self, user_name, token: str, v: str = '5.131'):
        self.token = token
        self.v = v
        self.user_id = self.get_user_id(user_name)

    def get_user_id(self, user_name):
        if user_name.isdigit():
            return user_name
        else:
            return str(requests.get('https://api.vk.com/method/utils.resolveScreenName',
                                    {'screen_name': f'{user_name}', 'access_token': f'{self.token}',
                                     'v': '5.131'}).json()['response']['object_id'])

    def get_albums(self, user_name):
        albums_ids = []
        user_id = self.get_user_id(user_name)
        url = 'https://api.vk.com/method/photos.getAlbums'
        params = {
            'access_token': self.token,
            'v': self.v,
            'owner_id': user_id,
            'need_system': 1
        }
        response = requests.get(url, params=params).json()
        logging.debug('Список альбомов получен')
        for album in response['response']['items']:
            albums_ids.append(album['id'])
        return albums_ids

    def get_photo(self, user_name, album, photo_count: int = 5):
        json_dict = {}
        user_id = self.get_user_id(user_name)
        url = 'https://api.vk.com/method/photos.get'
        params = {
            'access_token': self.token,
            'v': self.v,
            'album_id': f'{album}',
            'owner_id': user_id,
            'extended': '1',
            'count': f'{photo_count}'}
        response = requests.get(url, params=params).json()
        photo_dict = {}
        for item in response['response']['items']:
            max_height = 0
            photo_url = ''
            type_s = ''
            for size in item['sizes']:
                if size['height'] > max_height:
                    max_height = size['height']
                    photo_url = size['url']
                    type_s = size['type']
            if str(item['likes']['count']) in photo_dict:
                photo_dict[str(item['likes']['count']) + str(item['date'])] = photo_url
                json_dict['file_name'] = f"{str(item['likes']['count']) + str(item['date'])}.jpg"
            else:
                photo_dict[str(item['likes']['count'])] = photo_url
                json_dict['file_name'] = f"{item['likes']['count']}.jpg"
            json_dict['size'] = type_s
        logging.info(f'Список фото в альбоме {album} получен!')

        Vk_json_dict[album] = json_dict
        with open('vk_photos_dict.json', 'w', encoding='utf-8') as file:
            json.dump({'Vkontakte': Vk_json_dict}, file, indent=2)
        return photo_dict
