import datetime
import time

import pymysql

from DBUtils.PooledDB import PooledDB

pool = PooledDB(pymysql, 10, host='rm-hp3mz89q1ca33b2e37o.mysql.huhehaote.rds.aliyuncs.com', user='adi',
                password='Adi_mysql',
                database='adinsights_v3', charset='utf8')


pool1 = PooledDB(pymysql, 10, host='192.168.168.83', port=3306, user='root',
                 password='Adi_mysql',
                 database='adi', charset='utf8')

media_list = [
    {
        'mid': '1',
        'media_name': '微信朋友圈',
        'pkg_name': 'com.tencent.mm',
        'icon_url': 'http://47.95.217.37:8000/static/icon/53.png',
        'source_id': '3',
    },
    {
        'mid': '2',
        'media_name': '微信公众号',
        'pkg_name': 'com.tencent.mm',
        'icon_url': 'http://47.95.217.37:8000/static/icon/81.png',
        'source_id': '1',
    },
    {
        'mid': '3',
        'media_name': '快手',
        'pkg_name': 'com.smile.gifmaker',
        'icon_url': 'http://47.95.217.37:8000/static/icon/62.png',
        'source_id': '3',
    }
]


class mediaInfo_day:
    def __init__(self, start, end):
        self.start_time = start
        self.end_time = end

    def run(self):
        self.asy_day()

    def asy_day(self):
        for media_info in media_list:
            mid = media_info["mid"]
            media_name = media_info.get("media_name", "")
            pkg_name = media_info.get("pkg_name", "")
            icon_url = media_info.get("icon_url", "")
            source_id = media_info.get("source_id", "")

            for i in range(int(self.start_time), int(self.end_time) + 1):
                days = (datetime.date.today() + datetime.timedelta(days=-i)).strftime("%Y-%m-%d")

                flag = 0
                if str(mid) == str(3):
                    ks_sql = "SELECT phone,account,sum(amount) FROM ks_account where `day`='{days}' GROUP BY account "
                    ks_sql = ks_sql.format(days=days)
                    sql = ks_sql
                else:
                    pyq_sql = "SELECT account, COUNT(DISTINCT(fp)) as amount from wechat_account_ext WHERE source_id = '{source_id}' and `day` = '{day}' GROUP BY account"
                    pyq_sql = pyq_sql.format(day=days, source_id=source_id)
                    sql = pyq_sql
                    flag = 1
                data = self.select_adi(sql)
                if data:
                    data = list(data)
                    for item in data:
                        ks_id = ""
                        account = ""
                        count = ""
                        if item:
                            if flag == 0:
                                account = item[0]
                                if account == "(null)" and media_name == "快手":
                                    account = "未知"
                                ks_id = item[1]
                                if ks_id == "(null)":
                                    ks_id = "未知"
                                count = item[2]
                            elif flag == 1:
                                account = item[0]
                                count = item[1]
                                print(count)
                                ks_id = ""

                            select_sql = "SELECT counts FROM mediaInfo_day where account='{act}' and ks_id='{ks_id}' and days='{days}' and mediaUUID='{mid}';"
                            select_sql = select_sql.format(act=account, ks_id=ks_id, days=days, mid=mid)
                            select_msg = self.select_local(select_sql)
                            if select_msg:
                                update_sql = "UPDATE mediaInfo_day set counts='{counts}',update_time=NOW() where ks_id='{ks_id}' and account='{act}' and days='{days}' and mediaUUID='{mid}'"
                                update_sql = update_sql.format(act=account, counts=count, ks_id=ks_id, days=days,
                                                               mid=mid)
                                update_msg = self.excute_local(update_sql)
                                if update_msg:
                                    print(self.get_time_now(), media_name, account, " 更新成功")

                            else:
                                insert_sql = "INSERT into mediaInfo_day(account,days,appName,ks_id,bundleId,appIcon,counts,mediaUUID,insert_time) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,NOW())"
                                insert_param = [account, days, media_name, ks_id, pkg_name, icon_url, count, str(mid)]
                                msg = self.excute_local_param(insert_sql, insert_param)
                                if msg:
                                    print(self.get_time_now(), media_name, account, " 插入成功！")
                else:
                    print(self.get_time_now() + " " + str(media_name) + " 暂无数据更新")

    def get_time_now(self):
        return str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def select_adi(self, sql):
        try:
            conn = pool.connection()
            cursor = conn.cursor()
            cursor.execute(sql)
            raw = cursor.fetchall()
            cursor.close()
            conn.close()
            return raw
        except Exception as e:
            print(e)
            return 0

    def excute_local_param(self, sql, param):
        try:
            conn1 = pool1.connection()
            cursor = conn1.cursor()
            cursor.execute(sql, param)
            conn1.commit()
            cursor.close()
            conn1.close()
            return 1
        except Exception as e:
            print(e)
            return 0

    def select_local(self, sql):
        try:
            conn1 = pool1.connection()
            cursor = conn1.cursor()
            cursor.execute(sql)
            raw = cursor.fetchall()
            cursor.close()
            conn1.close()
            return raw
        except Exception as e:
            print(e)
            return 0

    def excute_local(self, sql):
        try:
            conn1 = pool1.connection()
            cursor = conn1.cursor()
            cursor.execute(sql)
            conn1.commit()
            cursor.close()
            conn1.close()
            return 1
        except Exception as e:
            print(e)
            return 0


if __name__ == '__main__':
    asy = mediaInfo_day(0, 1)
    while True:
        asy.run()
        time.sleep(300)
