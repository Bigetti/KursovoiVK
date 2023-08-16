import requests
import json
import os
import datetime
from vk import VK
from yandex_disk import YandexDisk


def main():

    

    vk_access_token = open("token_vk_access").read()
    # vk_user_id = open("token_user_id").read()
    yandex_disk_token = open("token").read()

    user_input = input("Enter user ID or screen name: ")
    user_id = None

    

    if user_input.isdigit():
        vk = VK(vk_access_token, user_input)  # Создание экземпляра класса VK
        user_info = vk.users_info()  # Вызов метода users_info через экземпляр класса
        if user_info and 'response' in user_info:
            
            print("User exists")
            print(user_info)
            vk_user_id = user_info['response'][0].get('id')
            if vk_user_id:
                print("VK User ID:", vk_user_id)
            else:
                print("Could not retrieve VK User ID")
        else:
            print("User does not exist")
    

    elif not user_input.isdigit():
        vk = VK(vk_access_token)
        vk_user_id = vk.get_user_id_by_screen_name(user_input)
        if vk_user_id:
            print("User exists")
        else:
            print("User does not exist")    
    
    
    
    if vk_user_id:


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