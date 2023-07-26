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
            'album_id': 'profile',
            'extended': 1
        }

        response = requests.get(url, params={**self.params, **params})
        photos_data = response.json()

        if 'error' in photos_data:
            print(f"Ошибка при получении фотографий VK: {photos_data['error']['error_msg']}")
            return None

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




    def put_fotos_to_yandex_disk(self, file_name, photo_url, yandex_disk_token):

        photos = self.vk_get_fotos()
        if not photos:
            return
        
        base_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
        folder_path = "/FotosVK/"
        url = f'{base_url}?path={folder_path}{file_name}'

        headers = {"Authorization": f"OAuth {yandex_disk_token}"}
        response = requests.post(url, headers=headers, params={"url": photo_url})
        if response.status_code == 202:
            print(f'Successfully uploaded {file_name} to Yandex.Disk')
            return True
        else:
            print(f'Failed')
            return False

        

def main():

    vk_access_token = open("token_vk_access").read()
    vk_user_id = open("token_user_id").read()
    yandex_disk_token = open("token").read()


    vk = VK(vk_access_token, vk_user_id)

    res_info = vk.users_info()
    print(res_info)
    print()

    photos = vk.vk_get_fotos()
    if not photos:
        print("Couldn't gain photos from VK")
        return
    # print(res_foto)

    photos.sort(key=lambda x: (x['likes']['count'], x['date']), reverse = True)

    max_photos_to_save = 5
    photos_to_save = photos[:max_photos_to_save]



    for photo in photos_to_save:
        if 'url' in photo:
            photo_url = photo['url']
            file_name = photo['path'].split('/')[-1]
            vk.put_fotos_to_yandex_disk(photo_url, photo["path"], yandex_disk_token)
        else:
            print(f"Фотография с ID {photo['id']} не содержит информации об URL и будет пропущена.")


    result_data = []
    
    for photo in photos_to_save:
        if 'url' in photo:
            file_name = photo['path'].split('/')[-1]
            photo_info = {"file_name": file_name, "size": "z"}
            result_data.append(photo_info)
        else:
            print(f"Фотография с ID {photo['id']} не содержит информации об URL и будет пропущена.")



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



  ###Данные для непрямого использования в программе
# vk_pril_id = 51711680

# vk_link = 'https://oauth.vk.com/authorize?client_id=51711680&scope=65536&response_type=token'

# access_token_link_vk = '''https://oauth.vk.com/blank.html#access_token=vk1.a.5nnLMTio2eDDLhxQECDI28O5tIn0Azfm6trhgALV0JwMSvxTZlEkiGydZLy9YXeh2N2NuxGoyMc8cy9gUX8-K3Bhs_Ug-zD4mgZYg4AcRQ0qrr5F2OLsReAHPjBWvyD5K1
# gC_6YYi48jKZVONpc0zEOehlXFpc6JNdANZpBgmnuxOxTB-528mD-ZQWGG7WJ0zYvIW0xFOwDhjqpOxurchsWQ&expires_in=0&user_id=1716063'''

 