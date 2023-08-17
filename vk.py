import requests
import datetime
import os

class VK:

    def __init__(self, vk_access_token, vk_user_id, version='5.131'):
       self.token = vk_access_token
       self.id = vk_user_id
       self.version = version
       self.params = {'access_token': self.token, 'v': self.version}
     

    def users_info(self):
       url = 'https://api.vk.com/method/users.get'
       params = {'user_ids': self.id}
       response = requests.get(url, params={**self.params, **params})
       return response.json()



    def vk_get_fotos(self):
        url = f"https://api.vk.com/method/photos.get"
        params = {
            'owner_id': self.id,
            'album_id': '170109067',
            'extended': 1
        }

        response = requests.get(url, params={**self.params, **params})
        photos_data = response.json()

        if 'error' in photos_data:
            print(f"Ошибка при получении фотографий VK: {photos_data['error']['error_msg']}")
            return None
        

        # Отладочный вывод для просмотра данных фотографий
        # for photo in photos_data['response']['items']:
        #     print(photo)
           

        return photos_data['response']['items']
    


    # Этого нет в задании это эксперимент с загрузкой фото сначала на пк, чтобы понять где сбой
    def download_photos_to_local(self, folder_path_local):
        photos = self.vk_get_fotos()
        if not photos:
            print("No photos found on VK.")
            return  # Выходим из метода, если нет фотографий

        # Создаем папку для сохранения фотографий на локальном компьютере
        os.makedirs(folder_path_local, exist_ok=True)

        for photo in photos:
            if 'sizes' in photo:
                # Получаем дату загрузки фотографии в формате UNIX timestamp
                upload_date = photo['date']
                upload_date_formatted = datetime.datetime.fromtimestamp(upload_date).strftime('%Y-%m-%d')
                
                # Формируем имя файла на основе количества лайков и даты загрузки
                likes_count = photo['likes']['count']
                unique_id = photo['id']
                
                file_name = f"{likes_count}_{upload_date_formatted}_{unique_id}.jpg"
                photo_url = photo['sizes'][-1]['url']
                
                local_file_path = os.path.join(folder_path_local, file_name)

                # Загружаем фотографию с VK
                response = requests.get(photo_url)
                if response.status_code in [200, 201]:
                    with open(local_file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Successfully downloaded {file_name} to {folder_path_local}")
                else:
                    print(f"Failed to download {file_name}")

            else:
                print(f"Фотография с ID {photo['id']} не содержит информации об URL и будет пропущена.")


