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


# Create your views here.

class ClassifyView(View):
    def get(self, request):
        return render(request, 'index.html', {})

    def post(self, request):
        json_data = request.POST.get("json_data", "")
        json_dict = {"key", "value"}
        return JsonResponse(json_dict)


class FormView(View):
    def get(self, request):
        return render(request, "article-list.html", {})

    def post(self, request):
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


class StatisticsView(View):
    def get(self, request):
        result = {}
        date_list = []
        android_data_list = []
        ios_data_list = []
        sum_data = []
        media_name = "天天快报"
        end_days = str(datetime.date.today())
        start_days = (datetime.date.today() + datetime.timedelta(days=-30)).strftime("%Y-%m-%d")
        sql = "select * from app_statistics where (days BETWEEN '{start_days}' and '{end_days}') and media_name='{media_name}' ORDER BY days"
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
        result = {
                "date_list": date_list,
                "android_data_list": android_data_list,
                "ios_data_list": ios_data_list,
                "sum_data": sum_data,
        }
        # result['date_list'] = date_list
        # result['android_data_list'] = android_data_list
        # result['ios_data_list'] = ios_data_list
        # result['sum_data'] = sum_data
        # print(result)
        return render(request, "console.html", {'data':json.dumps(result)})

    def post(self, request):
        # ua= 1 andrio 2 ios
        result = {}
        date_list = []
        android_data_list = []
        ios_data_list = []
        sum_data = []
        media_name = request.POST.get("media_name", "")
        report_type = request.POST.get("report_type", "")
        if media_name == "看点快报":
            media_name = "天天快报"
        end_days = str(datetime.date.today())
        start_days = (datetime.date.today() + datetime.timedelta(days=-30)).strftime("%Y-%m-%d")
        sql = ""
        if report_type=="game":
            sql = "select * from app_statistics where (days BETWEEN '{start_days}' and '{end_days}') and media_name='{media_name}' ORDER BY days"
        elif report_type=="app":
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
        result = {
            "result": {
                'date_list': date_list,
                "android_data_list": android_data_list,
                "ios_data_list": ios_data_list,
                "sum_data": sum_data,
            }
        }
        # print(result)

        return JsonResponse(result, safe=False)

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
