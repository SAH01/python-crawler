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
def get_iqy():
    #   获取数据库总数据条数
    conn, cursor = get_conn()
    sql = "select count(*) from movieiqy"
    cursor.execute(sql)     #   执行sql语句
    conn.commit()       #   提交事务
    all_num = cursor.fetchall()[0][0]       #cursor 返回值的类型是一个元祖的嵌套形式 比如( ( ) ,)
    pagenum=int(all_num/48)+1               #这里是计算一个下面循环的起始值    每48个电影分一组
    # print(pagenum)
    print("movieiqy数据库有", all_num, "条数据！")

    url = "https://pcw-api.iqiyi.com/search/recommend/list?channel_id=1&data_type=1&mode=11&page_id=1&ret_num=48&session=ee4d98ebb4e8e44c8d4b14fa90615fb7"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    }
    # response=requests.get(url=url,headers=headers)
    # response.encoding="utf-8"
    # page_text=response.text
    # print(page_text)
    """
    """
    #
    temp_list = []      #暂时存放单部电影的数据
    dataRes = []        #每次循环把单部电影数据放到这个list
    for i in range(1, 137):         #循环1-136 第137 json 是空的 也就是全部爬完
        url = "https://pcw-api.iqiyi.com/search/recommend/list?channel_id=1&data_type=1&mode=11&page_id=1&ret_num=48&session=ee4d98ebb4e8e44c8d4b14fa90615fb7"
        url_0 = "https://pcw-api.iqiyi.com/search/recommend/list?channel_id=1&data_type=1&mode=11&page_id="
        url_0 = url_0 + str(i) + "&ret_num=48&session=ad1d98bb953b7e5852ff097c088d66f2"
        print(url_0)        #输出拼接好的url
        response = requests.get(url=url_0, headers=headers)
        response.encoding = "utf-8"
        try:
            page_text = response.text
            #解析json对象
            json_obj = json.loads(page_text)
            #这里的异常捕获是因为     测试循环的次数有可能超过电影网站提供的电影数 为了防止后续爬到空的json对象报错
            json_list = json_obj['data']['list']
        except:
            print("捕获异常！")
            return dataRes          #json为空 程序结束
        for j in json_list:         #   开始循环遍历json串
            # print(json_list)
            name = j['name']        #找到电影名
            print(name)
            temp_list.append(name)
            #异常捕获，防止出现电影没有评分的现象
            try:
                score = j['score']      #找到电影评分
                print(score)
                temp_list.append(score)
            except KeyError:
                print( "评分---KeyError")
                temp_list.append("iqy暂无评分")            #替换字符串

            link = j['playUrl']             #找到电影链接
            temp_list.append(link)
            # 解析播放状态
            """
            独播：https://www.iqiyipic.com/common/fix/site-v4/video-mark/only.png
            VIP：https://pic0.iqiyipic.com/common/20171106/ac/1b/vip_100000_v_601_0_21.png
            星钻：https://www.iqiyipic.com/common/fix/site-v4/video-mark/star-movie.png
            """
            state = []
            pay_text = j['payMarkUrl']         #因为播放状态只有在一个图片链接里有 所以需要使用re解析出类似vip和only（独播）的字样
            print(pay_text)
            if (len(pay_text) == 0):            #如果没有这个图片链接 说明电影是免费播放
                state="免费"
            else:
                find_state = re.compile("(.*?).png")
                state = re.findall(find_state, pay_text)        #正则匹配链接找到vip
                # print(state[0])

                if(len(state)!=0):              #只有当链接不为空再执行
                    # print(state)
                    # 再次解析
                    part_state=str(state[0])
                    part_state=part_state.split('/')
                    print(part_state[-1])
                    state = part_state[-1][0:3]      #字符串分片
                    # 这里只输出了三个字符，如果是独播，页面显示的是only，我们设置为”独播“
                    if (state == "onl"):
                        state = "独播"
                    if (state == "sta"):
                        state = "星钻"
                    if(state == "vip"):
                        state="VIP"
            print(state)
            # 添加播放状态
            # print(state)
            temp_list.append(state)
            dataRes.append(temp_list)
            # print(temp_list)
            temp_list = []

        print('___________________________')
    return dataRes

def insert_iqy():
    cursor = None
    conn = None
    try:
        count=0
        list = get_iqy()
        print(f"{time.asctime()}开始插入爱奇艺电影数据")
        conn, cursor = get_conn()
        sql = "insert into movieiqy (id,name,score,path,state) values(%s,%s,%s,%s,%s)"
        for item in list:
            print(item)
            count = count + 1
            if (count % 48 == 0):
                print('___________________________')
            #异常捕获，防止数据库主键冲突
            try:
                cursor.execute(sql, [0, item[0], item[1], item[2], item[3] ])
            except pymysql.err.IntegrityError:
                print("重复！跳过！")

        conn.commit()  # 提交事务 update delete insert操作
        print(f"{time.asctime()}插入爱奇艺电影数据完毕")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)
    return;

if __name__ == '__main__':
    # get_iqy()
    insert_iqy()