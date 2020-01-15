import json
import math
import time

from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.db import connection
import redis
import pymysql

from DBUtils.PooledDB import PooledDB

pool = PooledDB(pymysql, 10, host='rm-hp3mz89q1ca33b2e37o.mysql.huhehaote.rds.aliyuncs.com', user='adi',
                password='Adi_mysql',
                database='adinsights_v3', charset='utf8')
conn = pool.connection()


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
            msg = json_data.get("msg", "")
            if str(msg) == "1":
                md5_id = json_data.get("md5", "")
                redis_handle = self.get_redis()
                redis_handle.lpush("pyq_ios", md5_id)
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
                        if item:
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
                            tmp["md5"] = item[11]
                            tmp_list.append(tmp)
                    except Exception as e:
                        print(e)
                pd["pbData"] = tmp_list
                pd["xmlData"] = []
                ad_json["data"] = pd
                # ad_json['from'] = media
                ad_json['msg'] = "success"
                return ad_json
            else:
                return {"msg": "data is not exist"}
        else:
            return {"msg": "request err"}

    def select_account(self, account):
        try:
            cursor = connection.cursor()
            sql_str = "SELECT username,media_id,dt,buttom,nickname,lp,creative,appstore_link,sbType,images,ad_id,union_md5 FROM wechat_res  where product='no_product' and phone=%s"
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
            md5_id = data.get("md5", "")
            if user and product and md5_id:
                status_code = self.update_product(product, str(user), str(md5_id))
                if status_code:
                    return {"msg": 'succes', "md5": md5_id}
                else:
                    return {"msg": "add product fail"}
            else:
                return {"msg": "user or product or uid is None!"}
        return {"msg": "data is None"}

    def update_product(self, product, account, md5_id):
        try:
            cursor = connection.cursor()
            sql_str = "UPDATE wechat_res SET product='{product}',tag=1,update_time=NOW() where phone='{account}' and union_md5='{md5_id}'"
            sql = sql_str.format(product=product, account=account, md5_id=md5_id)
            r = cursor.execute(sql)
            return r
        except Exception as e:
            print('update product error:', e)

    def get_redis(self):
        rdp_local = redis.ConnectionPool(host='127.0.0.1', port=6379, db=2)
        rdc_local = redis.StrictRedis(connection_pool=rdp_local)
        return rdc_local


class MediaInfo(View):

    def get(self, request):
        id = request.GET.get('id', "")
        user = request.GET.get('user', "")
        begin = request.GET.get('user', "")
        end = request.GET.get('end', "")
        index = request.GET.get('index', "")
        size = request.GET.get('size', "")
        mediaUUID = request.GET.get("mediaUUID", "")
        if str(id) == "1":
            json_data = self.get_all_data(user)
            return JsonResponse(json_data, safe=True)
        elif str(id) == "2":
            json_data = self.get_rank(begin, end)
            return JsonResponse(json.dumps(json_data), content_type="application/json", safe=False)
        elif str(id) == "3":
            json_data = self.adRecordDetail(user, begin, end, index, size, mediaUUID)
            return JsonResponse(json.dumps(json_data), content_type="application/json", safe=False)

    def post(self, request):
        pass

    def get_all_data(self, user):
        json_data = {}
        tmp = []

        for i in range(1, 4):
            flag = 0
            sql = "SELECT appName,bundleId,appIcon,defaultPrice,income,mediaUUID,SUM(counts) FROM mediaInfo_day where account='{user}' and mediaUUID='{mid}' GROUP BY appName"
            sql = sql.format(user=user, mid=str(i))
            data = self.select_data(sql)
            if data:
                data = list(data)
                result = data[0]
                if result:
                    tmp_data = {}
                    result = list(result)
                    tmp_data["appName"] = result[0]
                    tmp_data["bundleId"] = result[1]
                    tmp_data["appIcon"] = result[2]
                    tmp_data['mediaUUID'] = result[5]
                    defaultPrice = result[3]
                    count = result[6]
                    if count:
                        count = int(count)
                    if str(result[5]) == "3":
                        sql_income = "SELECT counts FROM mediaInfo_day where account='{account}' and mediaUUID='3'"
                        sql_income=sql_income.format(account=user)
                        income_result = self.select_data(sql_income)
                        for item in income_result:
                            if item:
                                counts = item[0]
                                if int(counts) >= 40:
                                    flag += 1
                        if not defaultPrice:
                            defaultPrice = 10
                        else:
                            defaultPrice = int(defaultPrice)
                        income = int(defaultPrice) * flag
                    else:
                        if not defaultPrice:
                            defaultPrice = 1
                        if not count:
                            count = 0
                        income = int(defaultPrice) * int(count)

                    tmp_data["count"] = count
                    tmp_data["defaultPrice"] = defaultPrice
                    tmp_data["income"] = income
                    tmp.append(tmp_data)

        if tmp:
            json_data["stats"] = "0"
            json_data["msg"] = "成功"
            json_data["data"] = tmp
        else:
            json_data["stats"] = "-1"
            json_data["msg"] = "当前无数据！"
            json_data["data"] = tmp
        return json_data

    def get_rank(self, begin, end):
        result = {}
        data = {}
        tmp, account_list, defaultPrice = self.get_rank_pyq(begin, end)
        pyq_list = self.process_pyq(tmp, account_list, defaultPrice)
        ks = self.get_rank_ks(begin, end)
        ks_list = self.process_ks(ks)
        data["1"] = pyq_list
        data["3"] = ks_list
        result["stats"] = "0"
        result["msg"] = "成功"
        result["data"] = data
        return result

    def get_rank_pyq(self, begin, end):
        tmp = {}
        defaultPrice = ""
        account_list = []
        sql = "SELECT account,sum(counts) as s,defaultPrice FROM mediaInfo_day where mediaUUID='1' and days BETWEEN '{A}' and '{B}' GROUP BY account ORDER BY s desc"
        sql = sql.format(A=begin, B=end)
        items = self.select_data(sql)
        for item in items:
            item = list(item)
            account = item[0]
            counts = item[1]
            defaultPrice = item[2]
            account_list.append(account)
            if counts:
                counts = int(counts)
            sum_counts = tmp.get(account, "")
            if sum_counts:
                sum_counts = int(sum_counts)
                counts += sum_counts
            tmp[account] = counts
        return tmp, account_list, defaultPrice

    def get_rank_ks(self, begin, end):
        account_dict = {}
        data = []
        sql = "SELECT account,counts FROM mediaInfo_day where mediaUUID=3 and days BETWEEN '{A}' and '{B}'"
        sql = sql.format(A=begin, B=end)
        result = self.select_data(sql)
        if result:
            result = list(result)
            for item in result:
                account = item[0]
                counts = item[1]
                value = account_dict.get(account, "")
                if counts:
                    counts = int(counts)
                if value:
                    if counts >= 40:
                        value += 1
                        account_dict[account] = value
                else:
                    if counts > 40:
                        account_dict[account] = 1
        if account_dict:
            data = sorted(account_dict.items(), key=lambda x: x[1], reverse=True)
        return data

    def process_ks(self, ks):
        ks_sum = "SELECT sum(counts) FROM mediaInfo_day where mediaUUID=3 and account='{phone}'"
        sql_name = "SELECT realName FROM wechat_res where phone='{phone}'"
        ks_list = []
        if ks:
            for item in ks:
                ks_json = {}
                account = item[0]
                days = item[1]
                ks_sql = ks_sum.format(phone=account)
                sum_count = self.select_data(ks_sql)
                if sum_count:
                    sum_count = list(sum_count)
                    sum_count = sum_count[0]
                    if sum_count:
                        sum_count = int(sum_count[0])
                else:
                    sum_count = 0
                if days:
                    days = int(days)
                else:
                    days = 0
                sql = sql_name.format(phone=account)
                name = self.select_data(sql)
                if not name:
                    name = ""
                else:
                    name = name[0]
                    if name:
                        if name:
                            name = "**" + str(name[-1])
                        else:
                            name = ""
                    else:
                        name = ""

                income = days * 10
                ks_json["phone"] = account
                ks_json["realName"] = name
                ks_json["income"] = income
                ks_json["submitCount"] = sum_count
                ks_json["vaildCount"] = sum_count
                ks_list.append(ks_json)
            return ks_list
        else:
            return []

    def process_pyq(self, tmp, account_list, defaultPrice):
        sql_name = "SELECT realName FROM wechat_res where phone='{phone}'"
        pyq_list = []
        if tmp and account_list:
            for account in account_list:
                tmp_json = {}
                sql = sql_name.format(phone=account)
                name = self.select_data(sql)
                if not name:
                    name = ""
                else:
                    name = name[0]
                    if name:
                        name = name[0]
                        if name:
                            name = "**" + str(name[-1])
                        else:
                            name = ""
                    else:
                        name = ""
                counts = tmp[account]
                if counts:
                    counts = int(counts)
                else:
                    counts = 0
                if not defaultPrice:
                    defaultPrice = 1
                else:
                    defaultPrice = int(defaultPrice)
                if account and len(account) == 11:
                    account = str(account[0:3]) + "xxxx" + str(account[-3:])
                income = defaultPrice * counts
                tmp_json["phone"] = account
                tmp_json["realName"] = name
                tmp_json["income"] = income
                tmp_json["submitCount"] = counts
                tmp_json["vaildCount"] = counts
                pyq_list.append(tmp_json)
            return pyq_list
        else:
            return []

    def adRecordDetail(self, user, begin, end, index, size, mediaUUID):
        final_json = {}

        if user and str(mediaUUID):
            result_list = []
            sql = "SELECT username,media_id,dt,buttom,nickname,lp,creative,appstore_link,sbType,images,ad_id,union_md5,insert_time,product FROM wechat_res  where phone='{user}' and days BETWEEN '{begin}' and '{end}' ORDER BY days desc"
            sql = sql.format(user=user, begin=begin, end=end)
            data = self.select_data(sql)
            if data:
                result = list(data)
                for i in result:
                    item = list(i)
                    tmp = {}
                    ad_json = {}
                    pd = {}
                    tmp_list = []
                    try:
                        if item:
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
                            tmp["md5"] = item[11]
                            tmp_list.append(tmp)
                            pd["pbData"] = tmp_list
                            pd["xmlData"] = []
                            insert_time = item[12]
                            product = item[13]
                            if product == "no_product":
                                status = 1
                            else:
                                status = 0
                            timeArray = time.strptime(str(insert_time), "%Y-%m-%d %H:%M:%S")
                            timeStamp = int(time.mktime(timeArray))
                            ad_json["adInfo"] = pd
                            ad_json["price"] = 1
                            ad_json["status"] = status
                            ad_json["submitTime"] = timeStamp
                            result_list.append(ad_json)
                    except Exception as e:
                        print(e)
                if not index:
                    index = 0
                else:
                    try:
                        index = int(index)
                    except:
                        index = 0
                if not size:
                    size = 5
                else:
                    try:
                        size = int(size)
                    except:
                        size = 5
                lens = len(result_list)
                sum_page = math.ceil(lens / size)
                if lens < int(size):
                    final_json["stats"] = "0"
                    final_json["msg"] = "成功"
                    final_json["data"] = result_list
                elif index > sum_page:
                    final_json["stats"] = "0"
                    final_json["msg"] = "成功"
                    final_json["data"] = []
                else:
                    start = (index * size)
                    end = ((index * size) + size)
                    if end >= lens:
                        end = lens
                    final_json["stats"] = "0"
                    final_json["msg"] = "成功"
                    final_json["data"] = result_list[start:end]
                return final_json
            else:
                final_json["stats"] = "-1"
                final_json["msg"] = "暂无数据"
                final_json["data"] = []
                return final_json
        else:
            final_json["stats"] = "-1"
            final_json["msg"] = "用户名或者媒体有误！"
            final_json["data"] = []
            return final_json

    def select_data(self, sql):
        cur = connection.cursor()
        cur.execute(sql)
        raw = cur.fetchall()
        return raw
