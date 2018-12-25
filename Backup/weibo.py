#!/usr/bin/python3

from urllib.parse import urlencode
import requests
from pyquery import PyQuery
from pymongo import MongoClient

base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2830678474',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

def get_page(page):
    params = {
        'type': 'uid',
        'value': '2830678474',
        'containerid': '1076032830678474',
        'page': page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)

def parse_page(json):
    if json:
        results = []
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            if item == None:
                continue
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['text'] = PyQuery(item.get('text')).text()
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comments'] = item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            results.append(weibo)
        return results

client = MongoClient()
db = client['weibo']
collection = db['weibo']

def save_to_mongo(results):
    if collection.insert_many(results):
        print('Saved to Mongo')

if __name__ == '__main__':
    i = 1
    for page in range(1, 11):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            print(i, result)
            i = i + 1
        save_to_mongo(results)
