import json
import time
import numpy
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View
import zerorpc
from w3lib.util import to_unicode
import ast
import datetime
from django.db import connection
import redis

rdp_local = redis.ConnectionPool(host='127.0.0.1', port=6379, db=6)
rdc_local = redis.StrictRedis(connection_pool=rdp_local)
media_dict = {
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
    "手机迅雷": "90",
    "车来了": "91",

}


# Create your views here.

class ClassifyView(View):
    # 主页，index
    def get(self, request):
        if request.user.is_authenticated:
            user = request.user
            return render(request, 'index.html', {'user': user})
        else:
            return render(request, 'login.html', {"msg": "请登录后查看！"})

    def post(self, request):
        if request.user.is_authenticated:
            json_data = request.POST.get("json_data", "")
            json_dict = {"key", "value"}
            return JsonResponse(json_dict)
        else:
            return render(request, 'login.html', {"msg": "请登录后查看！"})


class FormView(View):
    # 爬虫优化
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, "article-list.html", {})
        else:
            return render(request, 'login.html', {"msg": "请登录后查看！"})

    def post(self, request):
        if request.user.is_authenticated:
            zc = zerorpc.Client()
            zc.connect('tcp://39.104.76.66:8787')
            json_data = request.POST.get("json_data", "")
            lines = str(json_data).split("\n")

            # 去重前总量
            repeated_sum = len(lines)
            start_time = "00:00:00"
            end_time = "00:00:00"
            repeated = []
            err_line = []
            repeated_dict = {"1": 0, "2": 0}
            remover_repeated_dict = {"1": 0, "2": 0}
            for index, line in enumerate(lines):
                if "android" or "ios" in line:
                    tmp = {}
                    line = line.split()
                    if len(line) == 9:
                        if index == 0:
                            start_time = line[1]
                        if index == repeated_sum - 1:
                            end_time = line[1]
                        creative = line[8]
                        repeated.append(creative)
                    elif len(line) > 9:
                        if index == 0:
                            start_time = line[1]
                        if index == repeated_sum - 1:
                            end_time = line[1]
                        creative = ''.join(line[8:])
                        repeated.append(creative)
                    else:
                        err_line.append(index + 1)
                else:
                    err_line.append(index + 1)

            # 去重
            remover_repeated = list(set(repeated))
            remove_sum = len(remover_repeated)

            # 去重前游戏应用分类
            for ad in repeated:
                type_name = zc.predict(to_unicode(ad))
                if type_name == "游戏":
                    repeated_dict["1"] += 1
                else:
                    repeated_dict["2"] += 1
            # 去重后游戏应用分类
            for ad in remover_repeated:
                type_name = zc.predict(to_unicode(ad))
                if type_name == "游戏":
                    remover_repeated_dict["1"] += 1
                else:
                    remover_repeated_dict["2"] += 1
            # 计算运行时间
            start_date = datetime.datetime.strptime(str(start_time), '%H:%M:%S')
            end_date = datetime.datetime.strptime(str(end_time), '%H:%M:%S')
            run_time = str(end_date - start_date)
            result = {
                'sum': {
                    "repeated": repeated_sum,
                    "remove_repeated": remove_sum
                },
                "time": {
                    'start_time': start_time,
                    "end_time": end_time,
                    "run_time": run_time
                },
                "result": {
                    "repeated_dict": repeated_dict,
                    "remover_repeated_dict": remover_repeated_dict,
                },
                "err_line": err_line
            }
            return JsonResponse(result, safe=False)
        else:
            return render(request, 'login.html', {"msg": "请登录后查看！"})


class StatisticsView(View):
    # 媒体数据监测
    def get(self, request):
        if request.user.is_authenticated:
            result = self.index_data('app_statistics')
            android_list, ios_list, sum_data = self.get_per_hour(0)
            return render(request, "console.html", {
                'data': json.dumps(result),
                'hour_android_list': android_list,
                'hour_ios_list': ios_list,
                'hour_sum_data': sum_data,
            })
        else:
            return render(request, 'login.html', {"msg": "请登录后查看！"})

    def post(self, request):
        # ua= 1 andrio 2 ios
        if request.user.is_authenticated:
            result = {}
            date_list = []
            android_data_list = []
            ios_data_list = []
            sum_data = []
            media_name = request.POST.get("media_name", "")
            report_type = request.POST.get("report_type", "")
            if media_name == "所有媒体":
                if report_type == "game":
                    result = self.index_data('app_statistics')
                else:
                    result = self.index_data('app_statistics_app')
                date_list = result.get("date_list")
                android_data_list = result.get("android_data_list")
                ios_data_list = result.get("ios_data_list")
                sum_data = result.get("sum_data")
                hour_android_list, hour_ios_list, hour_sum_data = self.get_per_hour(0)
            else:
                if media_name == "看点快报":
                    media_name = "天天快报"
                if media_name == "bilibili":
                    media_name = "哔哩哔哩"
                end_days = str(datetime.date.today())
                start_days = (datetime.date.today() + datetime.timedelta(days=-30)).strftime("%Y-%m-%d")
                sql = ""
                if report_type == "game":
                    sql = "select * from app_statistics where (days BETWEEN '{start_days}' and '{end_days}') and media_name='{media_name}' ORDER BY days"
                elif report_type == "app":
                    sql = "select * from app_statistics_app where (days BETWEEN '{start_days}' and '{end_days}') and media_name='{media_name}' ORDER BY days"
                sql = sql.format(start_days=start_days, end_days=end_days, media_name=media_name)
                result = self.fetch_one(sql)
                for item in result:
                    if len(item) == 7:
                        dt = item[4]
                        ua = item[2]
                        data = item[3]
                        if dt not in date_list:
                            date_list.append(item[4])
                        if ua == "1":
                            android_data_list.append(data)
                        else:
                            ios_data_list.append(data)
                if len(android_data_list) == (len(ios_data_list)):
                    for i in range(0, len(android_data_list)):
                        sum_data.append(android_data_list[i] + ios_data_list[i])
                media_id = media_dict[media_name]
                hour_android_list, hour_ios_list, hour_sum_data = self.get_per_hour(media_id)
            result = {
                "result": {
                    'date_list': date_list,
                    "android_data_list": android_data_list,
                    "ios_data_list": ios_data_list,
                    "sum_data": sum_data,
                    'hour_android_list': hour_android_list,
                    'hour_ios_list': hour_ios_list,
                    'hour_sum_data': hour_sum_data,
                }
            }
            # print(result)

            return JsonResponse(result, safe=False)
        else:
            return render(request, 'login.html', {"msg": "请登录后查看！"})

    def get_per_hour(self, media_id):
        android_list = []
        ios_list = []
        sum_data = []
        hour = datetime.datetime.now().hour
        for i in range(0, int(hour) + 1):
            key_android = str(media_id) + ":" + "1:" + str(i)
            key_ios = str(media_id) + ":" + "2:" + str(i)
            data_android = rdc_local.get(key_android)
            data_ios = rdc_local.get(key_ios)
            if data_android:
                android_list.append(int(data_android))
            else:
                data_android = 0
                android_list.append(data_android)
            if data_ios:
                ios_list.append(int(data_ios))
            else:
                data_ios = 0
                ios_list.append(data_ios)
            sum_data.append(int(data_android) + int(data_ios))

        return android_list, ios_list, sum_data

    def index_data(self, table_name):
        date_list = []
        android_data_list = []
        ios_data_list = []
        sum_data = []
        end_days = str(datetime.date.today())
        start_days = (datetime.date.today() + datetime.timedelta(days=-30)).strftime("%Y-%m-%d")
        sql = "SELECT days,ua,SUM(data_volume) as sum_data from table_name_tmp where (days BETWEEN '{start_days}' and '{end_days}')and ua=1  GROUP BY days  UNION SELECT days,ua,SUM(data_volume) as sum_data from table_name_tmp where (days BETWEEN '{start_days}' and '{end_days}') and ua=2  GROUP BY days ORDER BY days"
        sql = sql.format(start_days=start_days, end_days=end_days).replace("table_name_tmp", table_name)
        result = self.fetch_one(sql)

        if result:
            for item in result:
                if len(item) == 3:
                    dt = item[0]
                    ua = item[1]
                    data = int(item[2])
                    if dt not in date_list:
                        date_list.append(dt)
                    if ua == "1":
                        android_data_list.append(data)
                    else:
                        ios_data_list.append(data)
            if len(android_data_list) == (len(ios_data_list)):
                for i in range(0, len(android_data_list)):
                    sum_data.append(android_data_list[i] + ios_data_list[i])
        result = {
            "date_list": date_list,
            "android_data_list": android_data_list,
            "ios_data_list": ios_data_list,
            "sum_data": sum_data,
        }
        return result

    def fetch_one(self, sql):
        cursor = connection.cursor()
        cursor.execute(sql)
        raw = cursor.fetchall()
        return raw

    def sum_game(self, media_name, ts):
        # 总游戏量
        sql_game_sum = "select media.name, count(report_game_new.id) as m_count from report_game_new JOIN media on report_game_new.media_id=media.id where report_game_new.day='{day}' and media.`name`='{media_name}' group by report_game_new.media_id order by count(report_game_new.id) desc"
        sql_game_sum = sql_game_sum.format(day=ts, media_name=media_name)
        fetch_sum_game = self.fetch_one(sql_game_sum)
        if fetch_sum_game and len(fetch_sum_game) > 0:
            sum_game = fetch_sum_game[1]
        else:
            sum_game = 0

        return sum_game

    def andriod_game(self, media_name, ts):
        sql_game = "select media.name, count(report_game_new.id) as m_count from report_game_new JOIN media on report_game_new.media_id=media.id where report_game_new.day='{day}' and media.`name`='{media_name}' and ua='{ua}' group by report_game_new.media_id order by count(report_game_new.id) desc"
        sql_game_andriod = sql_game.format(day=ts, media_name=media_name, ua=1)
        fetch_andriod_game = self.fetch_one(sql_game_andriod)
        if fetch_andriod_game and len(fetch_andriod_game) > 0:
            andriod_game = fetch_andriod_game[1]
        else:
            andriod_game = 0
        return andriod_game

    def ios_game(self, media_name, ts):
        sql_game = "select media.name, count(report_game_new.id) as m_count from report_game_new JOIN media on report_game_new.media_id=media.id where report_game_new.day='{day}' and media.`name`='{media_name}' and ua='{ua}' group by report_game_new.media_id order by count(report_game_new.id) desc"
        sql_game_ios = sql_game.format(day=ts, media_name=media_name, ua=2)
        fetch_ios_game = self.fetch_one(sql_game_ios)
        if fetch_ios_game and len(fetch_ios_game) > 0:
            ios_game = fetch_ios_game[1]
        else:
            ios_game = 0
        return ios_game

    def week_data(self, media_name):
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
            fetch_sum_game = self.fetch_one(sql_game_sum)
            if fetch_sum_game and len(fetch_sum_game) > 0:
                sum_game = fetch_sum_game[1]
            else:
                sum_game = 0
            data_list.append(sum_game)
        week_datatime_list = week_datatime_list[::-1]
        data_list = data_list[::-1]

        return week_datatime_list, data_list


class DownloadView(View):
    def get(self):
        pass

    def post(self):
        pass


class VersionView(View):
    def get(self, request):
        return render(request, 'version.html', {

        })

    def post(self, request):
        pass
