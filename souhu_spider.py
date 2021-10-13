import time
import traceback
import requests
from lxml import etree
import re
from bs4 import BeautifulSoup
from lxml.html.diff import end_tag
import json
import pymysql
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

def get_souhu():
    url='https://film.sohu.com/list_0_0_0_2_2_1_60.html?channeled=1200100000'
    #最新上架
    new_url='https://film.sohu.com/list_0_0_0_2_1_1_60.html?channeled=1200100000'
    #本周热播
    week_url='https://film.sohu.com/list_0_0_0_2_0_1_60.html?channeled=1200100000'
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }

    #初始化list
    templist=[]
    dataRes=[]
    #最受好评 一共30页 每页60部电影
    for i in range(1,31):
        url_1='https://film.sohu.com/list_0_0_0_2_2_'
        auto=str(i)
        url_2='_60.html?channeled=1200100000'
        url=url_1+auto+url_2
        response = requests.get(url, headers)
        response.encoding = 'utf-8'
        page_text = response.text
        # etree_ = etree.HTML(page_text)
        # 获取所有的li
        soup = BeautifulSoup(page_text, 'lxml')
        # 标签层级选择
        li_list = soup.select('.movie-list>li')
        print(len(li_list))
        if(len(li_list)==0):
            print("最受好评爬取结束！")
            if(len(dataRes)!=0):
                return dataRes
        for li in li_list:
            li_text=str(li)
            # print(li_text)
            li_soup=BeautifulSoup(li_text,'lxml')
            name=li_soup.find('div',class_="v_name_info").text
            #添加名字
            templist.append(name)
            # print(name)
            #添加评分
            score=li_soup.find('span',class_='v_score').text
            #处理评分
            score=score[-4:-1]
            templist.append(score)
            # print(score)
            #添加path
            path=li_soup.find('a',target="_blank")['href']
            templist.append(path)
            # print(path)
            #添加播放状态
            state="VIP"
            templist.append(state)
            print(templist)
            dataRes.append(templist)
            templist=[]
        print("-------------------------------------------")
    # print(len(dataRes))

    #最新上架

    templist = []
    for i in range(1,31):
        url_1='https://film.sohu.com/list_0_0_0_2_1_'
        auto=str(i)
        url_2='_60.html?channeled=1200100000'
        url=url_1+auto+url_2
        response = requests.get(url, headers)
        response.encoding = 'utf-8'
        page_text = response.text
        # etree_ = etree.HTML(page_text)
        # 获取所有的li
        soup = BeautifulSoup(page_text, 'lxml')
        # 标签层级选择
        li_list = soup.select('.movie-list>li')
        print(len(li_list))
        if(len(li_list)==0):
            print("最新上架爬取结束！")
            if(len(dataRes)!=0):
                return dataRes
        for li in li_list:
            li_text=str(li)
            # print(li_text)
            li_soup=BeautifulSoup(li_text,'lxml')
            name=li_soup.find('div',class_="v_name_info").text
            #添加名字
            templist.append(name)
            # print(name)
            #添加评分
            score=li_soup.find('span',class_='v_score').text
            #处理评分
            score=score[-4:-1]
            templist.append(score)
            # print(score)
            #添加path
            path=li_soup.find('a',target="_blank")['href']
            templist.append(path)
            # print(path)
            #添加播放状态
            state="VIP"
            templist.append(state)
            print(templist)
            dataRes.append(templist)
            templist=[]
        print("-------------------------------------------")
    # print(len(dataRes))
    #本周热播
    templist = []
    for i in range(1, 31):
        url_1 = 'https://film.sohu.com/list_0_0_0_2_0_'
        auto = str(i)
        url_2 = '_60.html?channeled=1200100000'
        url = url_1 + auto + url_2
        response = requests.get(url, headers)
        response.encoding = 'utf-8'
        page_text = response.text
        # etree_ = etree.HTML(page_text)
        # 获取所有的li
        soup = BeautifulSoup(page_text, 'lxml')
        # 标签层级选择
        li_list = soup.select('.movie-list>li')
        print(len(li_list))
        if (len(li_list) == 0):
            print("本周热播爬取结束！")
            if (len(dataRes) != 0):
                return dataRes
        for li in li_list:
            li_text = str(li)
            # print(li_text)
            li_soup = BeautifulSoup(li_text, 'lxml')
            name = li_soup.find('div', class_="v_name_info").text
            # 添加名字
            templist.append(name)
            # print(name)
            # 添加评分
            score = li_soup.find('span', class_='v_score').text
            # 处理评分
            score = score[-4:-1]
            templist.append(score)
            # print(score)
            # 添加path
            path = li_soup.find('a', target="_blank")['href']
            templist.append(path)
            # print(path)
            # 添加播放状态
            state = "VIP"
            templist.append(state)
            print(templist)
            dataRes.append(templist)
            templist = []
        print("-------------------------------------------")
    # print(len(dataRes))
    #list去重
    old_list = dataRes
    new_list = []
    for i in old_list:
        if i not in new_list:
            new_list.append(i)
    print(new_list)  # [2, 3, 4, 5, 1]
    return new_list
#插入数据库
def insert_souhu():
    cursor = None
    conn = None
    try:
        count=0
        list = get_souhu()
        print(f"{time.asctime()}开始插入搜狐电影数据")
        conn, cursor = get_conn()
        sql = "insert into moviesohu (id,name,score,path,state) values(%s,%s,%s,%s,%s)"
        for item in list:
            print(item)
            count = count + 1
            #异常捕获，防止数据库主键冲突
            try:
                cursor.execute(sql, [0, item[0], item[1], item[2], item[3] ])
            except pymysql.err.IntegrityError:
                print("重复！跳过！")
        conn.commit()  # 提交事务 update delete insert操作
        print(f"{time.asctime()}插入搜狐电影数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)
    return;

if __name__ == '__main__':
    # get_iqy()
    # get_souhu()
    insert_souhu()