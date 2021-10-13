import time
import traceback
import requests
from lxml import etree
import re
from bs4 import BeautifulSoup
from lxml.html.diff import end_tag
import json
import pymysql
#西瓜爬取失败 {'data': {'code': -1, 'message': '无效的referer'}}
def getxigua():
    url='https://www.ixigua.com/cinema/filter/dianying/?is_new_connect=0&is_new_user=0&paid=%E5%85%8D%E8%B4%B9&wid_try=2'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    urlforjson='https://www.ixigua.com/api/cinema/filterv2/albums?_signature=_02B4Z6wo00f01e6nkVAAAIDCXlZ9mU5sfPHug5XAABs478'
    response=requests.get(urlforjson,headers)
    response.encoding='utf-8'
    page_text=response.text
    json_res=json.loads(page_text)
    print(json_res)
    soup=BeautifulSoup(page_text,'lxml')
    etree_=etree.HTML(page_text)
    movie_all=etree_.xpath('//*[@id="App"]/div/div[2]/section/div')
    print(movie_all)
    return 1
    #免费第一页


if __name__ == '__main__':
    getxigua()