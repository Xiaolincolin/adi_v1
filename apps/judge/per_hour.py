import datetime

import pymysql
import redis
from DBUtils.PooledDB import PooledDB

rdp_local = redis.ConnectionPool(host='127.0.0.1', port=6379, db=6)
rdc_local = redis.StrictRedis(connection_pool=rdp_local)

pool = PooledDB(pymysql, 10, host='rm-hp3mz89q1ca33b2e37o.mysql.huhehaote.rds.aliyuncs.com', user='adi',
                password='Adi_mysql',
                database='adinsights_v3', charset='utf8')


media_name = {
    "360浏览器": "46",
    "hao123": "50",
    "IT之家": "41",
    "pptv": "23",
    "QQ浏览器": "54",
    "QQ空间": "75",
    "TapTap": "87",
    "UC头条": "5",
    "UC浏览器": "57",
    "vivo浏览器": "71",
    "wifi万能钥匙": "10",
    "zaker": "37",
    "一点资讯": "17",
    "东方头条": "42",
    "中关村在线": "44",
    "中华万年历": "74",
    "中央天气预报": "70",
    "乐视视频": "24",
    "今日十大热点": "27",
    "今日头条": "1",
    "今日影视大全": "73",
    "今日要看": "48",
    "优酷视频": "6",
    "凤凰新闻": "14",
    "凤凰视频": "19",
    "华为浏览器": "79",
    "咪咕影院": "51",
    "哔哩哔哩": "32",
    "唔哩头条": "67",
    "土豆视频": "34",
    "墨迹天气": "20",
    "天天快报": "9",
    "好奇心日报": "38",
    "好看视频": "56",
    "小米浏览器": "72",
    "小米画报": "83",
    "小米视频": "84",
    "引力资讯": "69",
    "微信-公众号": "89",
    "微信-小程序": "85",
    "微信-朋友圈": "53",
    "快手": "66",
    "悦头条": "40",
    "懂球帝": "18",
    "抖音": "33",
    "搜狐新闻": "16",
    "搜狐视频": "39",
    "搜狗搜索": "30",
    "搜狗浏览器": "26",
    "斗鱼": "86",
    "新浪体育": "25",
    "新浪微博": "49",
    "新浪新闻": "11",
    "新浪财经": "12",
    "最右": "77",
    "段友": "78",
    "汽车之家": "29",
    "波波视频": "47",
    "火山小视频": "58",
    "爱奇艺视频": "8",
    "爱看": "65",
    "猎豹浏览器": "21",
    "猎豹清理大师": "76",
    "球球视频": "36",
    "界面新闻": "28",
    "百度": "4",
    "百度浏览器": "31",
    "百度视频": "35",
    "百度贴吧": "55",
    "皮皮搞笑": "82",
    "皮皮虾": "81",
    "知乎": "80",
    "米尔军事": "59",
    "糗事百科": "60",
    "网易新闻": "2",
    "腾讯QQ": "88",
    "腾讯新闻": "3",
    "腾讯视频": "7",
    "虎扑": "22",
    "西瓜视频": "15",
    "豆瓣": "52",
    "趣头条": "13",
    "傲游浏览器": "45",
    "风行视频": "43",
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
