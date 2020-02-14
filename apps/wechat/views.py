import datetime
import json
import sys

from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection

# Create your views here.
from django.views import View



class WechatView(View):
    def get(self, request):
        if request.user.is_authenticated:
            year = datetime.datetime.now().year
            month = datetime.datetime.now().month
            month_len = len(str(month))
            if month_len == 1:
                month = '0' + str(month)
            this_month = str(year) + "-" + str(month)
            a_month_data = self.get_month_data(this_month)
            return render(request, "role.html", {"this_month": json.dumps(a_month_data)})
        else:
            return render(request, 'login.html', {"msg": "请登录后查看！"})

    def post(self, request):
        if request.user.is_authenticated:
            click_time = request.POST.get("click_time", "")
            dt_type = request.POST.get("dt_type", "")
            if dt_type == "m":
                days = click_time
                data_list = self.get_month_data(days)
                return JsonResponse(data_list, safe=False)
            else:
                days = click_time
                data_list = self.get_one_day(days)
                return JsonResponse(data_list, safe=False)
        else:
            return render(request, 'login.html', {"msg": "请登录后查看！"})

    def fetch_all(self, sql):
        cursor = connection.cursor()
        cursor.execute(sql)
        raw = cursor.fetchall()
        return raw

    def get_one_day(self, dt):
        sql = "SELECT * FROM wechat_asy where days='{}'"
        sql = sql.format(dt)
        data = self.fetch_all(sql)
        data_list = []
        for item in data:
            tmp = {}
            tmp["id"] = item[0]
            tmp["username"] = item[1]
            tmp["media"] = item[2]
            tmp["game"] = item[4]
            tmp["app"] = item[3]
            tmp["brand"] = item[5]
            tmp['days'] = item[8]
            data_list.append(tmp)
        return data_list

    def get_month_data(self, days):
        sql = "SELECT * FROM wechat_month_asy where days='{}'"
        sql = sql.format(days)
        data = self.fetch_all(sql)
        # print(data)
        data_list = []
        for item in data:
            tmp = {}
            tmp["id"] = item[0]
            tmp["username"] = item[1]
            tmp["media"] = ""
            tmp["game"] = item[3]
            tmp["app"] = item[2]
            tmp["brand"] = item[4]
            tmp['days'] = item[7]
            tmp['sum_day'] = item[8]
            data_list.append(tmp)

        return data_list
