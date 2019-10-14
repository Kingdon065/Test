#! python3

from urllib.parse import urlencode
import requests
import os, re
from hashlib import md5
from multiprocessing.pool import Pool

headers = {
    'referer': 'https://www.toutiao.com/search/?keyword=%E8%A1%97%E6%8B%8D%E7%BE%8E%E5%A5%B3',
    'x-requested-with': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
}

def get_page(offset):
    params = {
        'offset': offset,
        'format': 'json',
        'keyword': '街拍美女',
        'autoload': 'true',
        'count': 20,
        'cur_tab': 3,
        'from': 'search_tab'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError:
        return None

def get_images(json):
    items = json.get('data')
    regex_list = re.compile('/list/')
    if items:
        for item in items:
            title = item.get('title')
            images = item.get('image_list')
            if images == None:
                continue
            for image in images:
                url = 'http:' + regex_list.sub('/large/', image.get('url'))
                yield {
                    'image': url,
                    'title': title
                }

def save_image(item):
    title = item.get('title')
    if ':' in title:
        title = title.split(':')
        title = title[1]
    dirname = 'Images/{}'.format(title)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    try:
        response = requests.get(item.get('image'))
        if response.status_code == 200:
            file_path = '{0}/{1}.{2}'.format(dirname, md5(response.content).hexdigest(), 'jpg')
            if not os.path.exists(file_path):
                with open(file_path, 'wb') as f:
                    f.write(response.content)
            else:
                print('Already downloaded: ' + file_path)
    except requests.ConnectionError:
        print('Failed to save Image')

def main(offset):
    json = get_page(offset)
    for item in get_images(json):
        print(item)
        save_image(item)

GROUP_START = 0
GROUP_END = 5

if __name__ == '__main__':
    pool = Pool()
    groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    pool.map(main, groups)
    pool.close()
    pool.join()


