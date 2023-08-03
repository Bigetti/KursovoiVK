import requests
import json
import os
import pandas as pd



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
    

    def create_folder_on_yandex_disk(self, yandex_disk_token, folder_path):
        base_url = "https://cloud-api.yandex.net/v1/disk/resources"
        url = f'{base_url}?path={folder_path}'
        headers = {'Authorization': f'OAuth {yandex_disk_token}'}
        response = requests.put(url, headers=headers)

        if response.status_code in [200, 201]:
            print(f"Successfully created folder {folder_path} on Yandex.Disk")
        else:
            print(f"Failed to create folder {folder_path} on Yandex.Disk")




    def put_fotos_to_yandex_disk(self, file_name, yandex_disk_token):
        photos = self.vk_get_fotos()

        base_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        folder_path = "/FotosVK/"
        url = f'{base_url}?path={folder_path}{file_name}'

        headers = {"Authorization": f"OAuth {yandex_disk_token}"}

        for photo in photos:
            if 'sizes' in photo:
                # Ищем фотографию с размером 'r' (оригинал) в списке размеров фотографии
                photo_url = None
                for size in photo['sizes']:
                    if size["type"] == "r":
                        photo_url = size["url"]
                        break

                # Если удалось найти фотографию с размером 'r', загружаем ее на Яндекс.Диск
                if photo_url is not None:
                    response = requests.post(url, headers=headers, params={"url": photo_url, "overwrite": "true"})
                    # response = requests.put(url, headers=headers, data={"url": photo_url, "overwrite": "true"})
                    if response.status_code == 202:
                        print(f'Successfully uploaded {file_name} to Yandex.Disk')
                        return True
                    else:
                        print(f'Failed to upload {file_name} to Yandex.Disk')
                        return False
                else:
                    print(f"Фотография с ID {photo['id']} не содержит информации об URL размера 'r' и будет пропущена.")
            else:
                print(f"Фотография с ID {photo['id']} не содержит информации об URL и будет пропущена.")

        
    # Этого нет в задании это эксперимент с загрузкой фото сначала на пк, чтобы понять где сбой
    def download_photos_to_local(self, folder_path):
        photos = self.vk_get_fotos()
        if not photos:
            print("No photos found on VK.")
            return  # Выходим из метода, если нет фотографий

        # Создаем папку для сохранения фотографий на локальном компьютере
        os.makedirs(folder_path, exist_ok=True)

        for photo in photos:
            if 'sizes' in photo:
                photo_url = photo['sizes'][-1]['url']
                file_name = f"{photo['likes']['count']}_{photo['id']}.jpg"
                local_file_path = os.path.join(folder_path, file_name)

                # Загружаем фотографию с VK
                response = requests.get(photo_url)
                if response.status_code in [200, 201]:
                    with open(local_file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"Successfully downloaded {file_name} to {folder_path}")
                else:
                    print(f"Failed to download {file_name}")

            else:
                print(f"Фотография с ID {photo['id']} не содержит информации об URL и будет пропущена.")



def main():

    

    vk_access_token = open("token_vk_access").read()
    vk_user_id = open("token_user_id").read()
    yandex_disk_token = open("token").read()


    vk = VK(vk_access_token, vk_user_id)


    folder_path = r'F:\NETOLOGYPython\FotosVK'
    vk.download_photos_to_local(folder_path)

    res_info = vk.users_info()
    # print(res_info)
    print()

    photos = vk.vk_get_fotos()
    if not photos:
        print("Couldn't gain photos from VK")
        return
    

    
    # Данные из вункции Гет Фотос с ВК преобразуем в json file
    with open('vk_photos_data.json', 'w') as json_f:
        json.dump(photos, json_f, indent=4)


    photos.sort(key=lambda x: (x['likes']['count'], x['date']), reverse = True)

    max_photos_to_save = 5
    photos_to_save = photos[:max_photos_to_save]
    
    with open('vk_photos_to_save.json', 'w') as json_f:
        json.dump(photos_to_save, json_f, indent=4)
    # print(photos_to_save)

    df = pd.DataFrame(photos_to_save)
    excel_file_name = 'photos_to_save.xlsx'
    df.to_excel(excel_file_name, index=False)
    print(f"Data has been saved to {excel_file_name}")


    result_data = []

    for photo in photos_to_save:
        if 'sizes' in photo:
         
            file_name = f"{photo['likes']['count']}_{photo['id']}.jpg"
            vk.put_fotos_to_yandex_disk(file_name, yandex_disk_token)
            photo_info = {"file_name": file_name, "size": "z"}
            result_data.append(photo_info)

        else:
            print(f"Фотография с ID {photo['id']} не содержит информации об sizes и URL и будет пропущена.")


    # result_data = []
    
    # for photo in photos_to_save:
    #     if 'url' in photo:
    #         file_name = photo['path'].split('/')[-1]
    #         photo_info = {"file_name": file_name, "size": "z"}
    #         result_data.append(photo_info)
    #     else:
    #         print(f"Фотография с ID {photo['id']} не содержит информации об URL и будет пропущена.")



    with open('vk_photos.json', 'w') as json_f:
        json.dump(result_data, json_f, indent=4)

    df = pd.DataFrame(result_data)

    excel_file_name = 'vk_photos.xlsx'
    df.to_excel(excel_file_name, index=False)
    print(f"Data has been saved to {excel_file_name}")


    # # Преобразование списка словарей в DataFrame
    # df = pd.DataFrame(photos)

    # # Сохранение DataFrame в файл Excel
    # df.to_excel('res_foto.xlsx', index=False)



if __name__ == "__main__":
    main()