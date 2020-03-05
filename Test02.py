#! python3
# _*_ coding:utf-8 _*_

from PIL import Image

img = Image.open('01.jpg')
assert isinstance(img, Image.Image)
img.show()