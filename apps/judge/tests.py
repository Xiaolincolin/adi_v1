import datetime
import pymysql

# Create your tests here.
# for i in range(1, 7):
#     days = (datetime.date.today() + datetime.timedelta(days=-i)).strftime("%Y-%m-%d")
#     print(days)
connection = pymysql.connect(host='rm-hp3mz89q1ca33b2e37o.mysql.huhehaote.rds.aliyuncs.com', user='adi',
                             password='Adi_mysql',
                             database='adinsights_v3', charset='utf8')

# 得到一个可以执行SQL语句的光标对象
from .media_name.config import media_name


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



def yesterday_to_mysql():
    ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    today = str(datetime.date.today())
    days = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
    for name in media_name:

        try:
            android_sum = andriod_game(name, days)
            ios_sum = ios_game(name, days)
            if not android_sum:
                android_sum=0
            if not ios_sum:
                ios_sum=0
            sql = 'insert into app_statistics(media_name,ua,data_volume,days,add_time,update_time) values(%s,%s,%s,%s,%s,%s)'
            ios_param = [name, 'ios', ios_sum, days, ts, ts]
            insert_data(sql, ios_param)
            android_param = [name, 'android', android_sum, days, ts, ts]
            insert_data(sql, android_param)
            print(name+"同步完成！")
        except Exception as e:
            print(name+"报错了~")
            print(e)
    connection.commit()
    connection.close()

if __name__ == '__main__':
    yesterday_to_mysql()