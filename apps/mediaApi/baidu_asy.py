import datetime

# yesterday = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
# today = (datetime.date.today()).strftime("%Y-%m-%d")
#
# print(yesterday)
# print(today)
import random
import time

import pymysql
from DBUtils.PooledDB import PooledDB

pool = PooledDB(pymysql, 10, host='rm-hp3mz89q1ca33b2e37o.mysql.huhehaote.rds.aliyuncs.com', user='adi',
                password='Adi_mysql',
                database='adinsights_v3', charset='utf8')

pool1 = PooledDB(pymysql, 10, host='192.168.168.83', port=3306, user='root',
                 password='Adi_mysql',
                 database='adi', charset='utf8')
divce_id = {
    "_a2S8_aq28_qa28qiiBzaga92ugvhvtHjuXn8jPqBN0_iv8WoiSdiYuYvfgquB8g_l2h8luWSajBus8PYOvpIgajS8oIPBuflhvh": "KS002",
    "_a2S8_aq28_qa28q8ivh8_uJvulxhHucYiXT80u4vI08u2iqzuvHilitSigbu2a4Y02aigiRv8_VOXtzliv_N_ixv8zNPSixgC26": "KS003",
    "_a2S8_aq28_qa28qiiHSt_OzHtgpCBuO0uXf80uMvNY6P28Eoi2ougiIB8lSP28Q_l2haj8SBtlqOsa9_8vtIgiKSazk8HutgC-6": "KS004",
    "_a2S8_aq28_qa28q8aSR808PB8jhh2tH0iXt8gasvN0Y82fqo8Hkul8tHugha2ud_0H9a_8A2u0eOs89_PvCN_i728zIPvivjCvy": "KS005",
    "_a2S8_aq28_qa28qiavlagP_H8gFhHfY_uXfiluovN08iHuKoa-oiY8hSilYa2u7Y0Bz8Yip2f0ouXi0_iS3Ng8F2azZ8Sihgh-z": "KS006",
    "_a2S8_aq28_qa28q8uSSt_iIvulxh284guXn80aKvN0IO2uNoavzi0iJ2u_38HfHY0vh8_iR28gcus80luv2I_8x28oNi2fgghBY": "KS007",
    "_a2S8_aq28_qa28qii2za0uI-alxhvtDguXT8_auSNj8uHiOo8SJu0iM280euSat_0v0fgPWH80Lus8__avFIguuH8oIOHuTjh-z": "xiaoxia_2"

}


class Baidu:
    def __init__(self):
        pass

    def get_data_from_adi(self, ts):
        if not ts:
            ts = datetime.date.today().strftime("%Y-%m-%d")

        for dev_id, name in divce_id.items():
            tmp_all = 0
            tmp_game = 0
            tmp_app = 0
            sum_select_sql = "SELECT DISTINCT(material_id) FROM material_device where device_id='{dev_id}' and `day`='{dy}'".format(
                dev_id=dev_id, dy=ts)
            game_sql = "SELECT DISTINCT(n.material_id) FROM material_device as d,report_game_new as n where d.material_id=n.material_id and  d.device_id='{dev_id}' and d.`day`='{dy}'".format(
                dev_id=dev_id, dy=ts)
            app_sql = "SELECT DISTINCT(n.material_id) FROM material_device as d,report_app_new as n where d.material_id=n.material_id and  d.device_id='{dev_id}' and d.`day`='{dy}'".format(
                dev_id=dev_id, dy=ts)
            sum_result = self.select_data(sum_select_sql)
            if sum_result:
                sum_result = list(sum_result)
                tmp_all = len(sum_result)
            game_result = self.select_data(game_sql)
            if game_result:
                game_result = list(game_result)
                tmp_game = len(game_result)
            app_result = self.select_data(app_sql)
            if app_result:
                app_result = list(app_result)
                tmp_app = len(app_result)
            print()
            select_local = "select id from material_baidu where device_id='{dev_id}' and days='{ts}'".format(
                dev_id=dev_id, ts=ts)
            local_result = self.select_local(select_local)
            if local_result:
                update_sql = "update material_baidu set counts='{ct}',game='{game}',app='{app}',update_time=NOW() where device_id='{dev_id}'".format(
                    dev_id=dev_id, ct=tmp_all, game=tmp_game, app=tmp_app
                )
                info = self.select_local(update_sql)
                if info:
                    print(name + "更新成功")
                else:
                    print(name + "更新失败")
            else:
                insert_sql = "insert into material_baidu(device_id,counts,game,app,days,add_time) values (%s,%s,%s,%s,%s,now())"
                insert_info = self.insert_local(insert_sql, [dev_id, tmp_all, tmp_game, tmp_app, ts])
                if insert_info:
                    if insert_info:
                        print(name + "插入成功")
                    else:
                        print(name + "插入失败")

    def select_data(self, sql):
        try:
            conn = pool.connection()
            cur = conn.cursor()
            cur.execute(sql)
            raw = cur.fetchall()
            return raw
        except Exception as e:
            print("查数据有误", e)

    def select_local(self, sql):
        try:
            conn = pool1.connection()
            cur = conn.cursor()
            raw = cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            return raw
        except Exception as e:
            print("查数据有误", e)

    def insert_local(self, sql, param):
        try:
            conn = pool1.connection()
            cur = conn.cursor()
            raw = cur.execute(sql, param)
            conn.commit()
            cur.close()
            conn.close()
            return raw
        except Exception as e:
            print("插入数据有误", e)


if __name__ == '__main__':
    bd = Baidu()
    bd.get_data_from_adi("")
