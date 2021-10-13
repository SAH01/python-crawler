import time
import traceback
import requests
from lxml import etree
import re
from bs4 import BeautifulSoup
from lxml.html.diff import end_tag
import json
import pymysql
#爬取失败   乐视 json获取不到
def get_leshi():

    url='http://list.le.com/listn/c1_t-1_a-1_y-1_s1_lg-1_ph1_md_o4_d1_p.html'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
    }
    # response=requests.get(url,headers)
    # response.encoding='utf-8'
    # page_text=response.text
    # # print(page_text)
    # #每页30部 获取json
    # etree_=etree.HTML(page_text)
    # soup=BeautifulSoup(page_text,'lxml')
    # #获取所有dl
    # movie_all=soup.find_all('dl',class_="dl_movie")
    # # print(movie_all)
    # templist=[]
    # dataRes=[]
    # #添加
    # for dl in movie_all:
    #     # /html/body/div[3]/div/div[2]/dl[1]/dd[1]/a
    #     part_html=str(dl)
    #     part_soup=BeautifulSoup(part_html,'lxml')
    #     name=part_soup.find('a')['title']
    #     # print(name)
    #     templist.append(name)
    #     score=part_soup.find('span').text
    #     templist.append(score)
    #     # print(score)
    #     path=part_soup.find('a')['href']
    #     # print(path)
    #     templist.append(path)
    #     state="免费"
    #     templist.append(state)
    #     dataRes.append(templist)
    #     templist=[]
    # print(len(dataRes))
    #后面解析json数据
    json_url='http://list.le.com/getLesoData?from=pc&src=1&stype=1&ps=30&pn=2&ph=420001&dt=1&cg=1&or=4&stt=1&vt=180001&ispay=0&s=1'
    json_url_1='http://list.le.com/getLesoData?from=pc&src=1&stype=1&ps=30&pn='
    json_url_2='&ph=420001&dt=1&cg=1&or=4&stt=1&vt=180001&ispay=0&s=1'
    response_json=requests.get(json_url,headers)
    json_obj=json.loads(response_json.content.decode("utf-8"))
    print(json_obj)
    print(type(json_obj))
    print(json_obj['data'])
    # arr_list=json.loads(json_obj['data'])
    # print(type(arr_list))
    # print(arr_list[0]['name'])
    return
if __name__ == '__main__':
    get_leshi()