import requests
import datetime

class YandexDisk:

    
    def __init__(self, yandex_disk_token):
        
        self.token = yandex_disk_token
        self.params = {'access_token': self.token}
     

    def create_folder_on_yandex_disk(self, folder_path, yandex_disk_token):
        base_url = "https://cloud-api.yandex.net/v1/disk/resources"
        url = f'{base_url}?path={folder_path}'
        headers = {'Authorization': f'OAuth {yandex_disk_token}'}
       

        check_response = requests.get(url, headers=headers)
        if check_response.status_code == 200:
            print(f"Folder {folder_path} already exists on Yandex.Disk")
        else:
            create_response = requests.put(url, headers=headers)
            if create_response.status_code in [200, 201]:
                print(f"Successfully created folder {folder_path} on Yandex.Disk")
            else:
                print(f"Failed to create folder {folder_path} on Yandex.Disk")


    def put_fotos_to_yandex_disk(self, photos_to_save, folder_path, yandex_disk_token):

        base_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        headers = {"Authorization": f"OAuth {yandex_disk_token}"}
        
        
        for photo in photos_to_save:
            if 'sizes' in photo:
               # Получаем дату загрузки фотографии в формате UNIX timestamp
                upload_date = photo['date']
                upload_date_formatted = datetime.datetime.fromtimestamp(upload_date).strftime('%Y-%m-%d')
                
                # Формируем имя файла на основе количества лайков и даты загрузки
                likes_count = photo['likes']['count']
                unique_id = photo['id']
                found_x_size = False
                file_name = f"{likes_count}_{upload_date_formatted}_{unique_id}.jpg"

                url = f'{base_url}?path={folder_path}/{file_name}'
                photo_url = None

                for size in photo['sizes']:
                    if size["type"] == "x":
                        photo_url = size["url"]
                        # print(photo_url)
                        break

                if not photo_url:
                    print(f"Фотография с ID {photo['id']} не содержит информации об URL размера 'x' и будет пропущена.")
                    continue

                check_url = f"https://cloud-api.yandex.net/v1/disk/resources?path={folder_path}/{file_name}"
                check_response = requests.get(check_url, headers=headers)
                # check_response = requests.get(url, headers=headers)

                if check_response.status_code == 200:  # Файл существует, пропускаем
                    print(f"Фотография {file_name} уже существует на Яндекс.Диске, пропущена.")
                else:  # Файл не существует, загружаем новый
                    response = requests.post(url, headers=headers, params={"url": photo_url, "overwrite": "true"})
                    if response.status_code == 202:
                        print(f'Successfully uploaded {file_name} to Yandex.Disk')
                    else:
                        print(f'Failed to upload {file_name} to Yandex.Disk')