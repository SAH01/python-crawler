import requests
import json
from bs4 import BeautifulSoup       #网页解析获取数据
import sys
import re
import urllib.request,urllib.error #制定url，获取网页数据
import sqlite3
import xlwt     #excel操作
import time
import pymysql
import traceback
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

#爬取腾讯视频电影数据
def get_ten():
    conn,cursor=get_conn()
    sql="select count(*) from movieten"
    cursor.execute(sql)
    conn.commit()
    all_num=cursor.fetchall()[0][0]

    print("movieten数据库有",all_num,"条数据！")
    #   https://v.qq.com/channel/movie?listpage=1&channel=movie&sort=18&_all=1&offset=0&pagesize=30
    url="https://v.qq.com/channel/movie?listpage=1&channel=movie&sort=18&_all=1"        #链接
    param={                                                                             #参数字典
        'offset':0,
        'pagesize':30
    }
    headers={                                                                            #UA伪装
        'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '+
                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36'
    }
    # param['offset']=all_num
    offset = 0                                                                           #拼接url
    dataRes = []
    findLink = re.compile(r'href="(.*?)"')  # 链接
    findName = re.compile(r'title="(.*?)"')  # 影片名
    findScore= re.compile(r'<div class="figure_score">(.*?) </div>')        #评分
    #3*170
    for i in range(0,300):
        # res = urllib.request.urlopen(url)                             #urllib不推荐使用
        res = requests.get(url=url,params=param,headers=headers)       #编辑request请求
        # print(url)
        res.encoding='utf-8'                                           #设置返回数据的编码格式为utf-8
        html=BeautifulSoup(res.text,"html.parser")                      #BeautifulSoup解析
        part_html = html.find_all(r"a", class_="figure")               #找到整个html界面里a标签对应的html代码，返回值是一个list
        # print(part_html)
        if (len(part_html) == 0):
            print("页面返回空！")
            return dataRes
        offset = offset + 30                                            #修改参数字典+30部电影
        print("下面从第"+str(offset)+"部电影开始：")
        param['offset'] = offset
        print(param['offset'])
        for i in part_html:                                            #遍历每一个part_html
            # print(i)
            words = str(i)
            name=re.findall(findName, words)# 添加影片名
            score=re.findall(findScore, words)# 添加评分
            link=re.findall(findLink, words)# 添加链接
            findState=BeautifulSoup(words,'lxml')       #单独解析播放状态
            state=findState.select('a > img')           #找到img父级标签
            if(len(state)==1):                          #免费电影不存在播放状态的标志，所以当img长度是1的时候，需要补上一个空串
                state.append("")
            state_text=str(state[1])                    #拿到第二个img对应的内容，使用正则匹配到alt属性对应的字符串
            # print(state_text)
            temp_state=re.findall('<img alt="(.*?)"', state_text)
            if(len(temp_state)==0):
                temp_state.insert(0,"免费") # 添加播放状态---免费
            # print(temp_state[0])
            list_=[]
            if(len(score)==0):
                score.insert(0,"暂无评分")
            for i in dataRes:
                if name[0] in i[0]:
                    name.insert(0,name[0]+"（其他版本）")
            list_.append(name[0])
            list_.append(score[0])
            list_.append(link[0])
            list_.append(temp_state[0])
            # list_.append(statu)
            # print(list_)
            print(list_)
            dataRes.append(list_)
    # print(dataRes)      #打印最终结果
    # list=html.select(".figure_score")
    # for item in list:
    #     print(item)

    #把同一部电影的信息放到一个 [ ] 里面

    return dataRes
#插入到腾讯电影数据库
def insert_ten():
    """
    插入腾讯电影数据
    :return:
    """
    cursor = None
    conn = None
    try:
        list = get_ten()
        print(f"{time.asctime()}开始插入腾讯电影数据")
        conn, cursor = get_conn()
        sql = "insert into movieten (id,name,score,path,state) values(%s,%s,%s,%s,%s)"
        for item in list:
            try:
                cursor.execute(sql,[0,item[0],item[1],item[2],item[3]])
                print(item)
            except pymysql.err.IntegrityError:
                print("重复！跳过！")
        conn.commit()  # 提交事务 update delete insert操作
        print(f"{time.asctime()}插入腾讯电影数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)
    return ;
if __name__ == '__main__':
    # conn,cursor=get_conn()
    # list=[]
    # res_list=get_ten()
    # print(res_list)
    insert_ten()
