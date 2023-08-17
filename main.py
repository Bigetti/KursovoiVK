import requests
import json
import os
import datetime
from vk import VK
from yandex_disk import YandexDisk



def get_user_id_by_nickname(vk_access_token, nickname):
    params = {
        "access_token": vk_access_token,
        "v": "5.131",
        "screen_name": nickname
    }

    response = requests.get("https://api.vk.com/method/utils.resolveScreenName", params=params)
    data = response.json()
    print (data)

    # if "response" in data and data["response"]["type"] == "user":
    if "response" in data and isinstance(data["response"], dict) and data["response"]["type"] == "user":        
        return data["response"]["object_id"]
    else:
        return None

def get_user_id(vk_access_token, user_input):
    if user_input.isdigit():
        vk = VK(vk_access_token, user_input)
        user_info = vk.users_info()
        print(user_info)
        if user_info and 'response' in user_info and user_info['response']:
            vk_user_id = user_info['response'][0].get('id')
            return vk_user_id
        else:
            return None
    else:
        return get_user_id_by_nickname(vk_access_token, user_input)




def check_yandex_disk_token_validity(yandex_disk_token):
    headers = {
        "Authorization": f"OAuth {yandex_disk_token}"
    }

    response = requests.get("https://cloud-api.yandex.net/v1/disk", headers=headers)

    if response.status_code == 200:
        return True
    else:
        return False



def check_yandex_disk_token(max_attempts=3):
    for attempt in range(max_attempts):
        user_input = input(f"Enter your Yandex.Disk token (Attempt {attempt + 1}/{max_attempts}): ")

        if all(ord(c) < 128 for c in user_input):  # Проверяем, что все символы в строке имеют коды меньше 128
            if check_yandex_disk_token_validity(user_input):
                print("Yandex.Disk token is valid. Proceeding with the program.")
                return user_input
            else:
                print("Invalid Yandex.Disk token. Please try again.")
        else:
            print("Please enter the token using only Latin characters.")

    print("Maximum number of attempts reached. Exiting program.")
    return None



def main():

    

    vk_access_token = open("token_vk_access").read()
    # vk_user_id = open("token_user_id").read()
    # yandex_disk_token = open("token").read()

    yandex_disk_token = check_yandex_disk_token()

    if yandex_disk_token is None:
        return

 
    user_input = input("Enter user ID or screen_name: ")  # Запрос ввода ID или никнейма

    # Получение числового user_id через функцию get_user_id
    vk_user_id = get_user_id(vk_access_token, user_input)
    
    if vk_user_id is None:
        print("User does not exist")
        return

    print("User exists")
    print("VK User ID:", vk_user_id)

   
   

    vk = VK(vk_access_token, vk_user_id)

    yaD = YandexDisk(yandex_disk_token)


    # folder_path_local = r'F:\NETOLOGYPython\FotosVK'
    # vk.download_photos_to_local(folder_path_local)

    folder_path = r'/FotosVKGreatebyProgram'

    yaD.create_folder_on_yandex_disk(folder_path, yandex_disk_token)

    # res_info = vk.users_info()
    # # print(res_info)
    # print()

    photos = vk.vk_get_fotos()
    if not photos:
        print("Couldn't gain photos from VK")
        return
    

    
        # Данные из функции Гет Фотос с ВК преобразуем в json file
    with open('vk_photos_data.json', 'w') as json_f:
        json.dump(photos, json_f, indent=4)


    photos.sort(key=lambda x: (x['likes']['count'], x['date']), reverse = True)

    max_photos_to_save = 5
    photos_to_save = photos[:max_photos_to_save]
        
    with open('vk_photos_to_save.json', 'w') as json_f:
        json.dump(photos_to_save, json_f, indent=4)
        # print(photos_to_save)

        # df = pd.DataFrame(photos_to_save)
        # # excel_file_name = 'photos_to_save.xlsx'
        # # df.to_excel(excel_file_name, index=False)
        # print(f"Data has been saved to {excel_file_name}")

        
    yaD.put_fotos_to_yandex_disk(photos_to_save, folder_path, yandex_disk_token)

    result_data = []

    for photo in photos_to_save:
        if 'sizes' in photo:
                
            upload_date = photo['date']
            upload_date_formatted = datetime.datetime.fromtimestamp(upload_date).strftime('%Y-%m-%d')
                    
                    # Формируем имя файла на основе количества лайков и даты загрузки
            likes_count = photo['likes']['count']
            unique_id = photo['id']

            file_name = f"{likes_count}_{upload_date_formatted}_{unique_id}.jpg"                        
            photo_info = {"file_name": file_name, "size": "x"}
            result_data.append(photo_info)

        else:
            print(f"Фотография с ID {photo['id']} не содержит информации об sizes и URL и будет пропущена.")


    with open('vk_photos.json', 'w') as json_f:
        json.dump(result_data, json_f, indent=4)

        # df = pd.DataFrame(result_data)
        # excel_file_name = 'vk_photos.xlsx'
        # df.to_excel(excel_file_name, index=False)
        # print(f"Data has been saved to {excel_file_name}")


if __name__ == "__main__":
    main()