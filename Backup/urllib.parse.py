#!/usr/bin/python3

from urllib.parse import urlparse, urlunparse, urlsplit
from urllib.parse import urlunsplit, urlencode, parse_qs
from urllib.parse import parse_qsl
from urllib.parse import quote, unquote

url = 'http://www.baidu.com/index.html;user?id=5#comment'

result = urlparse(url, allow_fragments=False)
print(type(result), result, sep='\n')
print(result.scheme, result[0], result.netloc, result[1])

data = ['http', 'www.baidu.com', 'index.html', 'user', 'id=6', 'comment']
print(urlunparse(data))

result = urlsplit(url)
print(type(result), result, sep='\n')
print(result.scheme, result[0], result.netloc, result[1])

data2 = ['http', 'www.baidu.com', 'index.html', 'a=6', 'comment']
print(urlunsplit(data2))

params = {
    'name': 'germy',
    'age': 22
}
base_url = 'http://www.baidu.com?'
url = base_url + urlencode(params)
print(url)

query = 'name=germy&age=22'
print(parse_qs(query))
print(parse_qsl(query))

keyword = '壁纸'
url = 'https://www.baidu.com/s?wd=' + quote(keyword)
print(url)
print(unquote(url))

url  = 'https://www.baidu.com/s?wd=' + quote('编程')
print(url)
