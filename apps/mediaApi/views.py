import json

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.db import connection


class ApiView(View):
    def get(self, request):
        return "adi"

    def post(self, request):
        data = request.POST.get("data", "")
        do = request.POST.get("do", "")
        if str(do) == "1":
            json_data = self.get_data(data)
            return JsonResponse(json_data, safe=True)
        elif str(do) == "2":
            json_data = self.add_product(data)
            return JsonResponse(json_data, safe=True)
        else:
            return JsonResponse({"msg": "fail"}, safe=True)

    def get_data(self, json_data):
        data = json_data
        ad_json = {}
        tmp_usr = {}
        if data:
            if not isinstance(data, dict):
                data = json.loads(data)
            user = data.get("user", "")
            media = data.get("from", "")
            result = self.select_account(user)
            if result:
                for i in result:
                    item = list(i)
                    tmp = {}
                    try:
                        if item:
                            tmp['product'] = item[2]
                            tmp['images'] = item[3]
                            tmp['videos'] = item[4]
                            tmp['title'] = item[5]
                            tmp['media_id'] = item[6]
                            tmp['logo'] = item[7]
                            tmp['lp'] = item[8]
                            tmp['pkg_name'] = item[9]
                            tmp_usr[item[1]] = tmp
                    except Exception as e:
                        print(e)
                ad_json[user] = tmp_usr
                ad_json['from'] = media
                ad_json['msg'] = "success"
                return ad_json
            else:
                return {"msg": "data is not exist"}
        else:
            return {"msg": "request err"}

    def select_account(self, account):
        try:
            cursor = connection.cursor()
            sql_str = 'select * from wechat_tmp where `phone` = %s and product="no_product" '
            params = [account]
            cursor.execute(sql_str, params)
            data = cursor.fetchall()
            return data
        except Exception as e:
            print('select account error:', e)

    def add_product(self, json_data):
        data = json_data
        if data:
            if not isinstance(data, dict):
                data = json.loads(data)
            user = data.get("user", "")
            product = data.get("product", "")
            uid = data.get("ad_id", "")
            if user and product and uid:
                status_code = self.update_product(product, str(user), str(uid))
                if status_code:
                    return {"msg": 'succes'}
                else:
                    return {"msg": "add product fail"}
            else:
                return {"msg": "user or product or uid is None!"}
        return {"msg": "data is None"}

    def update_product(self, product, account, uid):
        try:
            cursor = connection.cursor()
            sql_str = "UPDATE wechat_tmp SET product='{product}',update_time=NOW() where phone='{account}' and ad_uid='{uid}'"
            sql = sql_str.format(product=product, account=account, uid=uid)
            r = cursor.execute(sql)
            return r
        except Exception as e:
            print('update product error:', e)
