import datetime
import json
import time

import pymysql
import requests

from DBUtils.PooledDB import PooledDB
from dingtalkchatbot.chatbot import DingtalkChatbot

pool = PooledDB(pymysql, 10, host='192.168.168.83', port=3306, user='root',
                password='Adi_mysql',
                database='adi', charset='utf8')
# webhook = 'https://oapi.dingtalk.com/robot/send?access_token=6e039d670b2ee0f9171759f7e03f259636ab9fe7a58dab8063cac70b8a3e64d0'
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=48270c497d9f1be54591ef820438454a1d312bacca3091662932e7b16a781430'
xiaoding = DingtalkChatbot(webhook)
at_mobiles = ['18295170578']


class Ration:
    def __init__(self):
        pass

    def fetch_all(self, sql):
        conn = pool.connection()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute(sql)
        raw = cursor.fetchall()
        cursor.close()
        conn.close()
        return raw

    def get_data(self):
        data_dict = {}
        yesterday_data = {}
        begin_day = (datetime.date.today() + datetime.timedelta(days=-1)).strftime("%Y-%m-%d")
        end_day = (datetime.date.today() + datetime.timedelta(days=-8)).strftime("%Y-%m-%d")
        select_sql = "SELECT days,media_name,data_volume FROM app_statistics where days BETWEEN '{end}' and '{start}'".format(
            start=begin_day, end=end_day)
        result = self.fetch_all(select_sql)
        if result:
            for item in result:
                media_name = item.get("media_name", "")
                data_valume = item.get("data_volume", 0)
                days = item.get("days", "")
                if days == begin_day:
                    media_num = yesterday_data.get(media_name)
                    if not media_num:
                        yesterday_data[media_name] = data_valume
                    else:
                        sum_num = int(data_valume) + (media_num)
                        yesterday_data[media_name] = sum_num
                else:
                    media_num = data_dict.get(media_name)
                    if not media_num:
                        data_dict[media_name] = data_valume
                    else:
                        sum_num = int(data_valume) + (media_num)
                        data_dict[media_name] = sum_num
            tmp_data = {}
            tmp_ratiom = {}
            important_ration = {}
            important_media_list = ['快手', '百度', '今日头条', '火山小视频', '西瓜视频', '抖音', '腾讯QQ', '腾讯视频', '腾讯新闻', '天天快报', '微信-朋友圈',
                                    '微信-小程序', '微信-公众号', '新浪微博', 'UC头条', 'UC浏览器']
            for media_name, num in yesterday_data.items():
                all_nums = data_dict.get(media_name)
                if str(all_nums) != '0':
                    avrage = round(int(all_nums) / 7, 3)
                    ration = round((num - avrage) / avrage, 3)
                    if media_name in important_media_list:
                        important_ration[media_name] = ration
                    else:
                        tmp_ratiom[media_name] = ration
                    tmp_data[media_name] = str(avrage) + "_" + str(num)
                else:
                    avrage = 0
                    ration = 0
                    # print(media_name, avrage, num, ration)
            sorted_data = sorted(tmp_ratiom.items(), key=lambda kv: (kv[1], kv[0]))
            important_media_sort = sorted(important_ration.items(), key=lambda kv: (kv[1], kv[0]))
            today = (datetime.date.today()).strftime("%Y-%m-%d")
            msg = str(today) + "游戏媒体增减率\n\n"
            msg += "媒体 七天平均值 昨日游戏量 增减率\n\n"
            for imp_per in important_media_sort:
                media_name = imp_per[0]
                ration = imp_per[1]
                avrage, num = str(tmp_data[media_name]).split("_")
                if "-" in str(ration):
                    strs = '<font color=#FF0000 size=4 face="宋体">{num}</font>'
                else:
                    strs = '<font color=#32CD32 size=4 face="宋体">+{num}</font>'
                if 0 < float(avrage) < 1:
                    avrage = 1
                msg += media_name + "  |   " + str(int(float(avrage))) + "  |   " + str(
                    num) + "     " + str(strs.format(
                    num=str(round(ration * 100, 2)) + "%")) + "\n\n"

            for per in sorted_data:
                media_name = per[0]
                ration = per[1]
                avrage, num = str(tmp_data[media_name]).split("_")
                if "-" in str(ration):
                    strs = '<font color=#FF0000 size=4 face="宋体">{num}</font>'
                else:
                    strs = '<font color=#32CD32 size=4 face="宋体">+{num}</font>'
                msg += media_name + "  |   " + str(int(float(avrage))) + "  |   " + str(
                    num) + "     " + str(strs.format(
                    num=str(round(ration * 100, 2)) + "%")) + "\n\n"
            mkd = {
                "msgtype": "markdown",
                "markdown": {
                    "title": str(today) + "游戏媒体增减率",
                    "text": msg
                },
                "at": {
                    "atMobiles": [
                        "18295170578"
                    ],
                    "isAtAll": False
                }
            }

            # print(mkd)
            headers = {'Content-Type': 'application/json;charset=utf-8'}
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            r = requests.post(webhook, data=json.dumps(mkd), headers=headers).json()
            code = r["errcode"]
            if code == 0:
                print(times + ":消息发送成功 返回码:" + str(code) + "\n")
            else:
                print(times + ":消息发送失败 返回码:" + str(code) + "\n")


if __name__ == '__main__':
    r = Ration()
    r.get_data()
