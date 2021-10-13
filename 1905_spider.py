import time
import traceback
import requests
from lxml import etree
import re
from bs4 import BeautifulSoup
from lxml.html.diff import end_tag
import json
import pymysql

def get1905():
    url='https://www.1905.com/vod/list/n_1/o3p1.html'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    templist=[]
    dataRes=[]
    #最热
    #1905电影网一共有99页，每页24部电影 for1-100 输出1-99页
    for i in range(1,100):
        url_1='https://www.1905.com/vod/list/n_1/o3p'
        auto=str(i)
        url_2='.html'
        url=url_1+auto+url_2
        print(url)
        response = requests.get(url, headers)
        response.encoding = 'utf-8'
        page_text = response.text
        soup = BeautifulSoup(page_text, 'lxml')
        # print(page_text)
        movie_all = soup.find_all('div', class_="grid-2x grid-3x-md grid-6x-sm")
        for single in movie_all:
            part_html=str(single)
            part_soup=BeautifulSoup(part_html,'lxml')
            #添加名字
            name=part_soup.find('a')['title']
            templist.append(name)
            # print(name)
            #添加评分
            try:
                score=part_soup.find('i').text
            except:
                if(len(score)==0):
                    score="1905暂无评分"
            templist.append(score)
            # print(score)
            #添加path
            path=part_soup.find('a',class_="pic-pack-outer")['href']
            templist.append(path)
            # print(path)
            #添加state
            state="免费"
            templist.append(state)
            print(templist)
            dataRes.append(templist)
            templist=[]
        print(len(dataRes))
    # print(movie_all)

    #---------------------------------------------
    #好评
    templist = []
    # 1905电影网一共有99页，每页24部电影 for1-100 输出1-99页
    for i in range(1, 100):
        url_1 = 'https://www.1905.com/vod/list/n_1/o4p'
        auto = str(i)
        url_2 = '.html'
        url = url_1 + auto + url_2
        print(url)
        response = requests.get(url, headers)
        response.encoding = 'utf-8'
        page_text = response.text
        soup = BeautifulSoup(page_text, 'lxml')
        # print(page_text)
        movie_all = soup.find_all('div', class_="grid-2x grid-3x-md grid-6x-sm")
        for single in movie_all:
            part_html = str(single)
            part_soup = BeautifulSoup(part_html, 'lxml')
            # 添加名字
            name = part_soup.find('a')['title']
            templist.append(name)
            # print(name)
            # 添加评分
            try:
                score = part_soup.find('i').text
            except:
                if (len(score) == 0):
                    score = "1905暂无评分"
            templist.append(score)
            # print(score)
            # 添加path
            path = part_soup.find('a', class_="pic-pack-outer")['href']
            templist.append(path)
            # print(path)
            # 添加state
            state = "免费"
            templist.append(state)
            print(templist)
            dataRes.append(templist)
            templist = []
        print(len(dataRes))
        #---------------------------------------------
        # 最新
        templist = []
        # 1905电影网一共有99页，每页24部电影 for1-100 输出1-99页
    for i in range(1, 100):
        url_1 = 'https://www.1905.com/vod/list/n_1/o1p'
        auto = str(i)
        url_2 = '.html'
        url = url_1 + auto + url_2
        print(url)
        response = requests.get(url, headers)
        response.encoding = 'utf-8'
        page_text = response.text
        soup = BeautifulSoup(page_text, 'lxml')
        # print(page_text)
        movie_all = soup.find_all('div', class_="grid-2x grid-3x-md grid-6x-sm")
        for single in movie_all:
            part_html = str(single)
            part_soup = BeautifulSoup(part_html, 'lxml')
            # 添加名字
            name = part_soup.find('a')['title']
            templist.append(name)
            # print(name)
            # 添加评分
            try:
                score = part_soup.find('i').text
            except:
                if (len(score) == 0):
                    score = "1905暂无评分"
            templist.append(score)
            # print(score)
            # 添加path
            path = part_soup.find('a', class_="pic-pack-outer")['href']
            templist.append(path)
            # print(path)
            # 添加state
            state = "免费"
            templist.append(state)
            print(templist)
            dataRes.append(templist)
            templist = []
        print(len(dataRes))
    #去重
    old_list = dataRes
    new_list = []
    for i in old_list:
        if i not in new_list:
            new_list.append(i)
            print(len(new_list))
    print("总数:     "+str(len(new_list)))
    return new_list
def insert_1905():
    cursor = None
    conn = None
    try:
        count = 0
        list = get1905()
        print(f"{time.asctime()}开始插入1905电影数据")
        conn, cursor = get_conn()
        sql = "insert into movie1905 (id,name,score,path,state) values(%s,%s,%s,%s,%s)"
        for item in list:
            print(item)
            # 异常捕获，防止数据库主键冲突
            try:
                cursor.execute(sql, [0, item[0], item[1], item[2], item[3]])
            except pymysql.err.IntegrityError:
                print("重复！跳过！")
        conn.commit()  # 提交事务 update delete insert操作
        print(f"{time.asctime()}插入1905电影数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)
    return;

#连接数据库  获取游标
def get_conn():
    """
    :return: 连接，游标
    """
    # 创建连接
    conn = pymysql.connect(host="127.0.0.1",
                    user="root",
                    password="000429",
                    db="movierankings",
                    charset="utf8")
    # 创建游标
    cursor = conn.cursor()  # 执行完毕返回的结果集默认以元组显示
    if ((conn != None) & (cursor != None)):
        print("数据库连接成功！游标创建成功！")
    else:
        print("数据库连接失败！")
    return conn, cursor
#关闭数据库连接和游标
def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()
    return 1

if __name__ == '__main__':
    # get1905()
    insert_1905()