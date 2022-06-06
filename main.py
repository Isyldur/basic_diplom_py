import requests
import Vk
import logging


class YaUpload:

    logging.basicConfig(filename='logging_file.log', filemode='w',  level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    def __init__(self, token):
        self.token = token

    def create_dir(self, dir_path):
        url = 'https://cloud-api.yandex.net/v1/disk/resources'
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        requests.put(url, params={'path': f'{dir_path}'}, headers=headers)

    def upload_photo(self, photo_dict: dict, path):
        headers = {'Content-Type': 'application/json', 'Authorization': f'OAuth {self.token}'}
        for name, url in photo_dict.items():
            params = {
                'path': f'{path}/{name}.jpg',
                'url': f'{url}'
            }
            requests.post(url='https://cloud-api.yandex.net/v1/disk/resources/upload', params=params, headers=headers)
            logging.info(f'Изображение {name}.jpg успешно загружено на диск!')

    def backup_photos(self, person, get_all=True):
        social = 'other'
        if isinstance(person, Vk.VkPhoto):  # сделал так чтобы работало и с одноклассниками, но пока что так
            social = 'Vkontakte'
        if get_all:
            albums_ids = person.get_albums(person.user_id)
            for album in albums_ids:
                try:
                    self.create_dir(f'Photo Backups/{social}/{album}')
                    logging.info(f'Папка Photo Backups/{social}/{album} создана')
                except Exception as err:
                    print(err)
                album_photo_dict = person.get_photo(person.user_id, album)
                logging.info('Начинаю загрузку файлов')
                self.upload_photo(album_photo_dict, f'Photo Backups/{social}/{album}')
        else:
            try:
                self.create_dir(f'Photo Backups/{social}/profile')
                logging.error(f'Папка Photo Backups/{social}/profile создана')
            except Exception as err:
                print(err)
            logging.info('Начинаю загрузку файлов')
            self.upload_photo(person.get_photo(person.user_id, 'profile'), f'Photo Backups/{social}/profile')


if __name__ == '__main__':
    oktoken = ''
    vktoken = ''
    begvk = Vk.VkPhoto('begemot_korovin', vktoken)
    ya_token = ''
    ya = YaUpload(ya_token)
    ya.backup_photos(begvk)
    # ya.backup_photos(begvk, False)

