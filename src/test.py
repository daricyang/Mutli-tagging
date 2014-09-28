# encoding: utf-8
__author__ = 'pok'

import urllib

data = '%7B%22gender%22%3A-1%2C%22roles%22%3A%5B%22%E6%95%B0%E7%A0%81%E6%8E%A7%22%5D%2C%22ans%22%3A%5B%5D%7D'
print urllib.unquote(data)
data = {"gender": -1, "roles": ["数码控"], "ans": []}
print urllib.quote(str(data))
