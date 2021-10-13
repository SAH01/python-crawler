import time
import traceback
import requests
from lxml import etree
import re
from bs4 import BeautifulSoup
from lxml.html.diff import end_tag
import json
import pymysql

#Top 100
#爬取猫眼失败 网页获取不到 每页json数据
def get_top100():
    url='https://maoyan.com/board/4'
    headers={
        'User-Agehnt':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    response=requests.get(url,headers)
    response.encoding='utf-8'
    print(response.text)
if __name__ == "__main__":
    get_top100()