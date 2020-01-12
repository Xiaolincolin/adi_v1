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
        try:
            json_dic = eval(request.body)
        except Exception as e:
            print(e)
            return JsonResponse({"msg": "body not a json"}, safe=True)
        data = json_dic.get("data", "")
        do = json_dic.get("do", "")
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
        pd = {}
        tmp_list = []
        if data:
            if not isinstance(data, dict):
                data = json.loads(data)
            user = data.get("user", "")
            # media = data.get("from", "")
            print("user", user)
            result = self.select_account(user)
            if result:
                for i in result:
                    item = list(i)
                    tmp = {}
                    try:
                        if item and len(item) == 11:
                            images = []
                            imgs = item[9]
                            if imgs and ",," in imgs:
                                imgs = str(imgs).split(",,")
                                for img in imgs:
                                    images.append(img)
                            elif imgs:
                                images.append(imgs)
                            tmp["imgs"] = images
                            tmp["username"] = item[0]
                            tmp['from'] = item[1]
                            dt = item[2]
                            if dt:
                                dt = str(dt).split("_")
                                if len(dt) == 2:
                                    tmp['adDisplayTime'] = dt[0]
                                    tmp['adCreateTime'] = dt[1]

                            tmp['adActionLinkName'] = item[3]
                            tmp['adUserNickName'] = item[4]
                            tmp['adActionLink'] = item[5]
                            tmp['adDescription'] = item[6]
                            tmp['adActionAppStoreLink'] = item[7]
                            tmp['subType'] = item[8]
                            tmp['advertiseID'] = item[10]
                            tmp_list.append(tmp)
                    except Exception as e:
                        print(e)
                pd["pbData"] = tmp_list
                pd["xmlData"] = []
                ad_json["data"] = pd
                # ad_json['from'] = media
                ad_json['msg'] = "1"
                return ad_json
            else:
                return {"msg": "data is not exist"}
        else:
            return {"msg": "request err"}

    def select_account(self, account):
        try:
            cursor = connection.cursor()
            sql_str = "SELECT username,media_id,dt,buttom,nickname,lp,creative,appstore_link,sbType,images,ad_id FROM wechat_res  where product='no_product' and phone=%s"
            # sql_str = 'select * from wechat_tmp where `phone` = %s and product="no_product" '
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
            ad_id = data.get("ad_id", "")
            if user and product and ad_id:
                status_code = self.update_product(product, str(user), str(ad_id))
                if status_code:
                    return {"msg": '1'}
                else:
                    return {"msg": "add product fail"}
            else:
                return {"msg": "user or product or uid is None!"}
        return {"msg": "data is None"}

    def update_product(self, product, account, ad_id):
        try:
            cursor = connection.cursor()
            sql_str = "UPDATE wechat_res SET product='{product}',update_time=NOW() where ad_id=(SELECT ad_id FROM wechat_user where phone='{account}' and ad_id='{uid}');"
            sql = sql_str.format(product=product, account=account, uid=ad_id)
            r = cursor.execute(sql)
            return r
        except Exception as e:
            print('update product error:', e)
