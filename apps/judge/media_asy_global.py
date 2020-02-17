import datetime
import time

import pymysql

from DBUtils.PooledDB import PooledDB

pool = PooledDB(pymysql, 10, host='35.241.64.108', user='adi_mysql',
                password='gengjiahong',
                database='adinsights', charset='utf8')

pool1 = PooledDB(pymysql, 10, host='192.168.168.83', port=3306, user='root',
                 password='Adi_mysql',
                 database='adi', charset='utf8')

# 得到一个可以执行SQL语句的光标对象
media_name = [
    "Vungle",
    "Adcolony",
    "Mopub",
    "Applovin",
    "Chartboost",
    "Facebook",
    "Unity",
    "Admob",
    "Audience Network",
    "Facebook(FB)",
    "Twitter",
    "SmartNews_Japan",
    "YahooNews_Japan",
    "Youtube",
    "TopBuzz",
    "Tik Tok",
    "BuzzVideo",
    "Ameba",
    "IronSource",
    "Pinterest",
    "Instagram",
    "Messenger",
    "Mobvista",
]


def fetch_one(sql):
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    raw = cursor.fetchone()
    cursor.close()
    conn.close()
    return raw


def insert_data(sql, param):
    conn1 = pool1.connection()
    cursor = conn1.cursor()
    cursor.execute(sql, param)
    conn1.commit()
    cursor.close()
    conn1.close()


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


def andriod_app(media_name, ts):
    sql_game = "select media.name, count(report_app_new.id) as m_count from report_app_new JOIN media on report_app_new.media_id=media.id where report_app_new.day='{day}' and media.`name`='{media_name}' and ua='{ua}' group by report_app_new.media_id order by count(report_app_new.id) desc"
    sql_game_andriod = sql_game.format(day=ts, media_name=media_name, ua=1)
    fetch_andriod_game = fetch_one(sql_game_andriod)
    if fetch_andriod_game and len(fetch_andriod_game) > 0:
        andriod_game = fetch_andriod_game[1]
    else:
        andriod_game = 0
    return andriod_game


def ios_app(media_name, ts):
    sql_game = "select media.name, count(report_app_new.id) as m_count from report_app_new JOIN media on report_app_new.media_id=media.id where report_app_new.day='{day}' and media.`name`='{media_name}' and ua='{ua}' group by report_app_new.media_id order by count(report_app_new.id) desc"
    sql_game_ios = sql_game.format(day=ts, media_name=media_name, ua=2)
    fetch_ios_game = fetch_one(sql_game_ios)
    if fetch_ios_game and len(fetch_ios_game) > 0:
        ios_game = fetch_ios_game[1]
    else:
        ios_game = 0
    return ios_game


def yesterday_to_mysql():
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    days = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    # days = "2019-12-14"
    for name in media_name:

        try:
            android_sum = andriod_game(name, days)
            ios_sum = ios_game(name, days)
            if not android_sum:
                android_sum = 0
            if not ios_sum:
                ios_sum = 0
            sql = 'insert into app_statistics_global(media_name,ua,data_volume,days,add_time,update_time) values(%s,%s,%s,%s,%s,%s)'
            ios_param = [name, '2', ios_sum, days, ts, ts]
            insert_data(sql, ios_param)
            android_param = [name, '1', android_sum, days, ts, ts]
            insert_data(sql, android_param)
            print("游戏:" + name + "同步完成！")
        except Exception as e:
            print("游戏:" + name + "报错了~")
            print(e)


def a_month_asn():
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today = str(datetime.date.today())
    for i in range(2, 30):
        print("正在同步第" + str(i) + "天")
        days = (datetime.date.today() + datetime.timedelta(days=-i)).strftime("%Y-%m-%d")
        for name in media_name:
            try:
                android_sum = andriod_game(name, days)
                ios_sum = ios_game(name, days)
                if not android_sum:
                    android_sum = 0
                if not ios_sum:
                    ios_sum = 0
                sql = 'insert into app_statistics_global(media_name,ua,data_volume,days,add_time,update_time) values(%s,%s,%s,%s,%s,%s)'
                ios_param = [name, '2', ios_sum, days, ts, ts]
                insert_data(sql, ios_param)
                android_param = [name, '1', android_sum, days, ts, ts]
                insert_data(sql, android_param)
                print(name + "同步完成！")
            except Exception as e:
                print(name + "报错了~")
                print(e)


def app_yesterday_to_mysql():
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today = str(datetime.date.today())
    days = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    # days = "2019-12-14"
    for name in media_name:

        try:
            android_sum = andriod_app(name, days)
            ios_sum = ios_app(name, days)
            if not android_sum:
                android_sum = 0
            if not ios_sum:
                ios_sum = 0
            sql = 'insert into app_statistics_app_global(media_name,ua,data_volume,days,add_time,update_time) values(%s,%s,%s,%s,%s,%s)'
            ios_param = [name, '2', ios_sum, days, ts, ts]
            insert_data(sql, ios_param)
            android_param = [name, '1', android_sum, days, ts, ts]
            insert_data(sql, android_param)
            print("应用:" + name + "同步完成！")
        except Exception as e:
            print("应用:" + name + "报错了~")
            print(e)


def app_a_month_asn():
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    for i in range(2, 30):
        print("正在同步第" + str(i) + "天")
        days = (datetime.date.today() + datetime.timedelta(days=-i)).strftime("%Y-%m-%d")
        for name in media_name:
            try:
                android_sum = andriod_app(name, days)
                ios_sum = ios_app(name, days)
                if not android_sum:
                    android_sum = 0
                if not ios_sum:
                    ios_sum = 0
                sql = 'insert into app_statistics_app_global(media_name,ua,data_volume,days,add_time,update_time) values(%s,%s,%s,%s,%s,%s)'
                ios_param = [name, '2', ios_sum, days, ts, ts]
                insert_data(sql, ios_param)
                android_param = [name, '1', android_sum, days, ts, ts]
                insert_data(sql, android_param)
                print(name + "同步完成！")
            except Exception as e:
                print(name + "报错了~")
                print(e)


if __name__ == '__main__':
    try:
        a_month_asn()
        # yesterday_to_mysql()
    except Exception as e:
        print("第一次失败：", e)
        time.sleep(10)
        try:
            print("重试！！！！")
            # yesterday_to_mysql()
            a_month_asn()
        except Exception as e:
            print("第二次失败：", e)

    try:
        # app_yesterday_to_mysql()
        app_a_month_asn()
    except Exception as e:
        print("第次失败：", e)
        time.sleep(10)
        try:
            print("重试！！！！")
            # app_yesterday_to_mysql()
            app_a_month_asn()
        except Exception as e:
            print("第二次失败：", e)
