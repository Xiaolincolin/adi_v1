import datetime
import pymysql
from django.test import TestCase
from adi.settings import *

# Create your tests here.
# for i in range(1, 7):
#     days = (datetime.date.today() + datetime.timedelta(days=-i)).strftime("%Y-%m-%d")
#     print(days)
connection = pymysql.connect(host='rm-hp3mz89q1ca33b2e37o.mysql.huhehaote.rds.aliyuncs.com', user='adi',
                             password='Adi_mysql',
                             database='adinsights_v3', charset='utf8')


# 得到一个可以执行SQL语句的光标对象


def sum_game(media_name, ts):
    # 总游戏量
    sql_game_sum = "select media.name, count(report_game_new.id) as m_count from report_game_new JOIN media on report_game_new.media_id=media.id where report_game_new.day='{day}' and media.`name`='{media_name}' group by report_game_new.media_id order by count(report_game_new.id) desc"
    sql_game_sum = sql_game_sum.format(day=ts, media_name=media_name)
    fetch_sum_game = fetch_one(sql_game_sum)
    if fetch_sum_game and len(fetch_sum_game) > 0:
        sum_game = fetch_sum_game[1]
    else:
        sum_game = 0

    return sum_game


def andriod_game(media_name, ts):
    sql_game = "select media.name, count(report_game_new.id) as m_count from report_game_new JOIN media on report_game_new.media_id=media.id where report_game_new.day='{day}' and media.`name`='{media_name}' and ua='{ua}' group by report_game_new.media_id order by count(report_game_new.id) desc"
    sql_game_andriod = sql_game.format(day=ts, media_name=media_name, ua=1)
    fetch_andriod_game = fetch_one(sql_game_andriod)
    if fetch_andriod_game and len(fetch_andriod_game) > 0:
        andriod_game = fetch_andriod_game[1]
    else:
        andriod_game = 0
    return andriod_game


def ios_game(media_name, ts):
    sql_game = "select media.name, count(report_game_new.id) as m_count from report_game_new JOIN media on report_game_new.media_id=media.id where report_game_new.day='{day}' and media.`name`='{media_name}' and ua='{ua}' group by report_game_new.media_id order by count(report_game_new.id) desc"
    sql_game_ios = sql_game.format(day=ts, media_name=media_name, ua=2)
    fetch_ios_game = fetch_one(sql_game_ios)
    if fetch_ios_game and len(fetch_ios_game) > 0:
        ios_game = fetch_ios_game[1]
    else:
        ios_game = 0
    return ios_game


def week_data(media_name):
    week_datatime_list = []
    data_list = []
    today = str(datetime.date.today())
    week_datatime_list.append(today)
    for i in range(1, 7):
        days = (datetime.date.today() + datetime.timedelta(days=-i)).strftime("%Y-%m-%d")
        week_datatime_list.append(days)
    for ts in week_datatime_list:
        sql_game_sum = "select media.name, count(report_game_new.id) as m_count from report_game_new JOIN media on report_game_new.media_id=media.id where report_game_new.day='{day}' and media.`name`='{media_name}' group by report_game_new.media_id order by count(report_game_new.id) desc"
        sql_game_sum = sql_game_sum.format(day=ts, media_name=media_name)
        fetch_sum_game = fetch_one(sql_game_sum)
        if fetch_sum_game and len(fetch_sum_game) > 0:
            sum_game = fetch_sum_game[1]
        else:
            sum_game = 0
        data_list.append(sum_game)
    week_datatime_list = week_datatime_list[::-1]
    data_list = data_list[::-1]

    return week_datatime_list, data_list


def fetch_one(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    raw = cursor.fetchone()
    return raw


def insert_data(sql, param):
    cursor = connection.cursor()
    cursor.execute(sql, param)
    connection.commit()



if __name__ == '__main__':
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today = str(datetime.date.today())
    days = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    andrio_data = andriod_game('天天快报', days)
    ios_data = ios_game('天天快报', days)
    # data = sum_game('天天快报', days)
    ua = 'ios'
    sql = 'insert into app_statistics(media_name,ua,data_volume,days,add_time,update_time) values(%s,%s,%s,%s,%s,%s)'
    param = ['天天快报', 'ios', ios_data, days, ts, ts]
    insert_data(sql, param)
    print(andrio_data, ios_data)
    print(ts)