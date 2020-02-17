import datetime

import pymysql
import redis
from DBUtils.PooledDB import PooledDB

rdp_local = redis.ConnectionPool(host='127.0.0.1', port=6379, db=7)
rdc_local = redis.StrictRedis(connection_pool=rdp_local)

pool = PooledDB(pymysql, 10, host='35.241.64.108', user='adi_mysql',
                password='gengjiahong',
                database='adinsights', charset='utf8')

media_name = {
    "Vungle": "1",
    "Adcolony": "2",
    "Mopub": "3",
    "Applovin": "4",
    "Chartboost": "5",
    "Facebook": "6",
    "Unity": "7",
    "Admob": "8",
    "Audience Network": "9",
    "Facebook(FB)": "10",
    "Twitter": "11",
    "SmartNews_Japan": "12",
    "YahooNews_Japan": "13",
    "Youtube": "14",
    "TopBuzz": "15",
    "Tik Tok": "16",
    "BuzzVideo": "17",
    "Ameba": "18",
    "IronSource": "19",
    "Pinterest": "20",
    "Instagram": "21",
    "Messenger": "22",
    "Mobvista": "23",
}


def asy_per_hour():
    android_data_sum = 0
    ios_data_sum = 0
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    hour = datetime.datetime.now().hour

    day = datetime.datetime.now().strftime('%Y-%m-%d')
    sql = "select media.name,ua, count(report_game_new.id) as m_count from report_game_new JOIN media on report_game_new.media_id=media.id where ua=1 and report_game_new.day='{day}' group by report_game_new.media_id UNION select media.name,ua, count(report_game_new.id) as m_count from report_game_new JOIN media on report_game_new.media_id=media.id where ua=2 and report_game_new.day='{day}' group by report_game_new.media_id ORDER BY m_count desc".format(
        day=day)
    raw_data = fetch_all(sql)
    if raw_data:
        for item in raw_data:
            media_tmp = ""
            try:
                if len(item) == 3:
                    media = item[0]
                    media_tmp = media
                    ua = item[1]
                    data = int(item[2])
                    if ua == 1:
                        android_data_sum += data
                    else:
                        ios_data_sum += data
                    media = media_name.get(media)
                    title = media + ":" + str(ua) + ":" + str(hour)
                    result = rdc_local.set(title, data)
            except Exception as e:
                print(e)
                print(media_tmp, "出错")
        title_android = "0:1:" + str(hour)
        title_ios = "0:2:" + str(hour)
        result_andriod = rdc_local.set(title_android, android_data_sum)
        if result_andriod:
            print(str(hour), "andriod of sum success")
        result_ios = rdc_local.set(title_ios, ios_data_sum)
        if result_ios:
            print(str(hour), "ios of sum success")


def fetch_all(sql):
    conn = pool.connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    raw = cursor.fetchall()
    cursor.close()
    conn.close()
    return raw


def get_per_hour(media_id):
    hour = datetime.datetime.now().hour
    key_android = str(media_id) + ":" + "1:" + str(hour)
    key_ios = str(media_id) + ":" + "2:" + str(hour)
    data_android = rdc_local.get(key_android)
    data_ios = rdc_local.get(key_ios)
    return data_android, data_ios


if __name__ == '__main__':
    data_android, data_ios = get_per_hour(0)
    if data_android or data_ios:
        print('同步正常')
    else:
        print("同步异常，再次同步！")
        try:
            ts = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            print(ts, "开始更新！")
            asy_per_hour()
            ts1 = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
            print(ts1, "更新结束！")
        except Exception as e:
            print(e)
            print("更新失败，再次更新")
            asy_per_hour()
