import re
import time
import traceback

from bs4 import BeautifulSoup
from lxml import etree
import pymysql
import requests
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
def get_imdb():

    # url='https://www.imdb.cn/feature-film/1-0-0-0/?page=1'
    headers={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
    }
    dataRes=[]      #最终结果集
    temp_list=[]        #暂时结果集

    # print(all_li)

    for i in range(1,202):
            url_='https://www.imdb.cn/feature-film/1-0-0-0/?page='+str(i)
            response = requests.get(url=url_, headers=headers)
            # print(response)
            response.encoding = 'utf-8'
            page_text = response.text
            # print(page_text)
            etree_ = etree.HTML(page_text)
            all_li = etree_.xpath('//div[@class="hot_box"]/ul/li')      #获取所有li
            #判断all_li是否为空
            if(len(all_li)==0):
                print("爬取结束，all_list为空！")
                if(len(dataRes)!=0):
                    return dataRes;
                else:
                    return ;
            print(url_)
            for li in all_li:
                name=li.xpath('./a[1]/img/@alt')
                if(len(name)==0):
                    name.append("电影名错误")
                # print(name)
                #存姓名
                temp_list.append(name[0])

                score=li.xpath('./span[@class="img_score"]/@title')
                if(len(score)==0):
                    score.append("imdb暂无评分")
                # print(score)
                #存分数
                temp_list.append(score[0])
                # print(temp_list)
                #存到dataRes 把temp_list置为空
                dataRes.append(temp_list)
                temp_list=[]
            # print(dataRes)
    return dataRes
def insert_imdb():
    """
        插入imdb数据
        :return:
        """
    cursor = None
    conn = None
    try:
        list_=[]
        list = get_imdb()
        if(type(list)!=type(list_)):
            return ;
        print(f"{time.asctime()}开始插入imdb数据")
        conn, cursor = get_conn()
        sql = "insert into movieimdb (id,name,score) values(%s,%s,%s)"
        for item in list:
            try:
                print(item)
                cursor.execute(sql, [0, item[0], item[1]])
            except pymysql.err.IntegrityError:
                print("重复！跳过！")
            conn.commit()  # 提交事务 update delete insert操作
            print(f"{time.asctime()}插入imdb数据完毕")
    finally:
        close_conn(conn, cursor)
    return;
# def get_dblen():
#     conn,cursor=
#     num_=

if __name__ == '__main__':
    # get_imdb()
    insert_imdb()