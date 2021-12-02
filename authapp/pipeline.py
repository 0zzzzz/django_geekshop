from datetime import datetime
import requests
from django.conf import settings
from social_core.exceptions import AuthForbidden
from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return
    url_method = 'https://api.vk.com/method/'
    access_token = response.get('access_token')
    fields = ','.join(['bdate', 'sex', 'about', 'photo_max_orig'])
    api_url = f'{url_method}users.get?fields={fields}&access_token={access_token}&v=5.131'
    response = requests.get(api_url)
    if response.status_code != 200:
        return
    data_json = response.json()['response'][0]
    print(data_json)

    if 'sex' in data_json:
        if data_json['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data_json['sex'] == 2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        else:
            user.shopuserprofile.gender = ShopUserProfile.OTHERS

    if 'about' in data_json:
        user.shopuserprofile.about = data_json['about']

    if 'bdate' in data_json:
        birthday = datetime.strptime(data_json['bdate'], '%d.%m.%Y').date()

        age = datetime.now().date().year - birthday.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')
        user.age = age

    if 'photo_max_orig' in data_json:
        url = data_json['photo_max_orig']
        db_file_path = f'users_avatars/{data_json["id"]}_{data_json["first_name"]}_{data_json["last_name"]}.{url.split(".")[-1]}'
        file_path = f'{settings.MEDIA_ROOT}/{db_file_path}'
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, 'wb') as avatar:
                avatar.write(response.content)
        user.avatar = db_file_path

    user.save()
