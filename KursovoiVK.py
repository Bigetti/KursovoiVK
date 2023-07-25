import requests
import json
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



    def vk_get_fotos(self, vk_user_id, vk_access_token):
        url = f"https://api.vk.com/method/photos.get"
        params = {
            'owner_id': vk_user_id,
            'album_id': 'profile',
            'extended': 1
        }

        response = requests.get(url, params={**self.params, **params})
        photos_data = response.json()

        if 'error' in photos_data:
            print(f"Ошибка при получении фотографий VK: {photos_data['error']['error_msg']}")
            return None

        return photos_data['response']['items']
        

def main():

    vk_access_token = open("token_vk_access").read()
    
    vk_user_id = open("token_user_id").read()

    yandex_disk_token = open("token").read()


    vk = VK(vk_access_token, vk_user_id)

    res_info = vk.users_info()
    print(res_info)
    print()

    res_foto = vk.vk_get_fotos(vk_user_id, vk_access_token)
    print(res_foto)



if __name__ == "__main__":
    main()



  ###Данные для непрямого использования в программе
# vk_pril_id = 51711680

# vk_link = 'https://oauth.vk.com/authorize?client_id=51711680&scope=65536&response_type=token'

# access_token_link_vk = '''https://oauth.vk.com/blank.html#access_token=vk1.a.5nnLMTio2eDDLhxQECDI28O5tIn0Azfm6trhgALV0JwMSvxTZlEkiGydZLy9YXeh2N2NuxGoyMc8cy9gUX8-K3Bhs_Ug-zD4mgZYg4AcRQ0qrr5F2OLsReAHPjBWvyD5K1
# gC_6YYi48jKZVONpc0zEOehlXFpc6JNdANZpBgmnuxOxTB-528mD-ZQWGG7WJ0zYvIW0xFOwDhjqpOxurchsWQ&expires_in=0&user_id=1716063'''

 