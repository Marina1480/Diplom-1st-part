# import pip
# import pyprind as pyprind
import requests
import time
# import sys
import json


URL_P = 'https://cloud-api.yandex.net/'
token_P =
headers_P = {'accept': 'application/json', 'authorization': f'OAuth {token_P}'}
token = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'


class Photosget():
    url = 'https://vk.com/begemot_korovin'

    def __init__(self, token, version=5.131):
        self.params = {
            'access_token': token,
            'v': version
        }

    def photos_get(self, token):
        params = {
            'access_token': token,
            'v': '5.131',
            'album_id': 'profile',
            'extended': 1,
            'photo_sizes': 1,
            'count': 5
        }

        req = requests.get('https://api.vk.com/method/photos.get', params).json()
        req = req['response']['items']
        # pprint(req)
        return req


vk_photos = Photosget(token)
res = vk_photos.photos_get(token)


files_name = []
for i in range(len(res)):
    if res[i-1]['likes']['count'] != res[i]['likes']['count']:
        files_name.append(str(res[i]['likes']['count']) + '.jpg')
    else:
        f_name = res[i]['likes']['count'], time.strftime("%d %b %Y", time.localtime(res[i]['date'])) + '.jpg'
        files_name.append(f_name)
print(files_name)

res_l = []
for i in range(len(res)):
    res_dict = {}
    res_dict['file_name'] = files_name[i]
    res_dict['size'] = res[i]['sizes'][-1]['type']
    res_l.append(res_dict)
    # print(res_dict)

print(res_l)

with open('Data.json', 'w') as f:
    json.dump(res_l, f)


url_k = "https://cloud-api.yandex.net/v1/disk/resources/"
params = {
    'path': 'New'
}

requests.put(url=url_k, params=params, headers=headers_P).json()

# from progress.bar import IncrementalBar
#
# bar = IncrementalBar('Bar', max=len(res))

for i in range(len(res)):
     photo_name = str(files_name[i])
     photo_url = res[i]['sizes'][-1]['url'] # загружаются не все фото. и каждый раз по-разному
     requests.post(URL_P + "v1/disk/resources/upload", headers=headers_P,
                  params={'path': 'New/' + photo_name, 'url': photo_url})
#     bar.next()
#     time.sleep(1)  # не визуализируется
#
# bar.finish()
