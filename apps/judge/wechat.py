import json
import datetime
import pymysql

from DBUtils.PooledDB import PooledDB

pool = PooledDB(pymysql, 10, host='rm-hp3mz89q1ca33b2e37o.mysql.huhehaote.rds.aliyuncs.com', user='adi',
                password='Adi_mysql',
                database='adinsights_v3', charset='utf8')
conn = pool.connection()


class wechat:
    def __init__(self):
        pass

    def get_data(self, days, source_id):
        sql = "SELECT account,type_id,source_id,COUNT(*) FROM wechat_account_ext a where `day`='{days}' and source_id='{source_id}' AND type_id=0  GROUP BY account UNION " \
              "SELECT account,type_id,source_id,COUNT(*) FROM wechat_account_ext a where `day` ='{days}' and source_id='{source_id}' AND type_id=1  GROUP BY account UNION " \
              "SELECT account,type_id,source_id,COUNT(*) FROM wechat_account_ext a where `day` = '{days}' and source_id='{source_id}' AND type_id=2  GROUP BY account;"
        sql = sql.format(days=days, source_id=source_id)
        fetch_data = self.fetch_all(sql)
        tmp = {}
        for item in fetch_data:
            print(item)
            user = item[0]
            type_id = item[1]
            source_id = item[2]
            sum_data = item[3]
            if user not in tmp:
                tmp[user] = {}

            if source_id == 0:
                tmp[user]['source_id'] = "小程序"
                tmp[user]['date_time'] = days
                tmp[user][type_id] = sum_data

            elif source_id == 1:
                tmp[user]['source_id'] = "公众号"
                tmp[user]['date_time'] = days
                tmp[user][type_id] = sum_data
            else:
                tmp[user]['source_id'] = "朋友圈"
                tmp[user]['date_time'] = days
                tmp[user][type_id] = sum_data

        return tmp

    def get_month_data(self, start_days, end_days):
        sql = "SELECT account,type_id,count(*) FROM wechat_account_ext where type_id=0 and `day` between '{start}' and '{end}' GROUP BY account UNION " \
              "SELECT account,type_id,count(*) FROM wechat_account_ext where type_id=1 and `day` between '{start}' and '{end}' GROUP BY account UNION " \
              "SELECT account,type_id,count(*) FROM wechat_account_ext where type_id=2 and `day` between '{start}' and '{end}' GROUP BY account  "

        sql = sql.format(start=start_days, end=end_days)
        fetch_data = self.fetch_all(sql)
        tmp = {}
        for item in fetch_data:
            # print(item)
            user = item[0]
            type_id = item[1]
            sum_data = item[2]
            if user not in tmp:
                tmp[user] = {}

            if type_id == 0:
                tmp[user]['days'] = '-'.join(str(start_days).split("-")[0:2])
                tmp[user][type_id] = sum_data

            elif type_id == 1:
                tmp[user]['days'] = '-'.join(str(start_days).split("-")[0:2])
                tmp[user][type_id] = sum_data
            else:
                tmp[user]['days'] = '-'.join(str(start_days).split("-")[0:2])
                tmp[user][type_id] = sum_data

        return tmp

    def fetch_all(self, sql):
        cursor = conn.cursor()
        cursor.execute(sql)
        raw = cursor.fetchall()
        return raw

    def asy_data(self):
        days = (datetime.date.today() + datetime.timedelta(days=-4)).strftime("%Y-%m-%d")
        source_id = [0, 1, 3]
        for s_id in source_id:
            data = self.get_data(days, s_id)
            if not data:
                continue
            for users, item in data.items():
                user = users
                source_id = item.get("source_id", "")
                date_time = item.get("date_time", "")
                app = item.get(0, 0)
                game = item.get(1, 0)
                brand = item.get(2, 0)
                sql = "insert into wechat_asy(users,source_id, app, game, brand, create_time, days) values(%s,%s,%s,%s,%s,%s,%s)"
                ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                params = [user, source_id, app, game, brand, ts, date_time]
                self.insert_data(sql, params)

    def asy_month_data(self):
        end_days = str(datetime.date.today())
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
        start_days = str(year) + "-" + str(month) + "-01"
        data = self.get_month_data(start_days, end_days)
        if not data:
            return
        for users, item in data.items():
            user = users
            days = item.get("days", "")
            app = item.get(0, 0)
            game = item.get(1, 0)
            brand = item.get(2, 0)
            sql = "insert into wechat_month_asy(users, app, game, brand, create_time, days) values(%s,%s,%s,%s,%s,%s)"
            ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            params = [user, app, game, brand, ts, days]
            self.insert_data(sql, params)

    def insert_data(self, sql, param):
        cursor = conn.cursor()
        cursor.execute(sql, param)


if __name__ == '__main__':
    we = wechat()
    # data = we.asy_data()
    we.asy_month_data()
    conn.commit()
    conn.close()
