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


# conn = pool.connection()
divce_id = {
    "_a2S8_aq28_qa28qiiBzaga92ugvhvtHjuXn8jPqBN0_iv8WoiSdiYuYvfgquB8g_l2h8luWSajBus8PYOvpIgajS8oIPBuflhvh": "KS002",
    "_a2S8_aq28_qa28q8ivh8_uJvulxhHucYiXT80u4vI08u2iqzuvHilitSigbu2a4Y02aigiRv8_VOXtzliv_N_ixv8zNPSixgC26": "KS003",
    "_a2S8_aq28_qa28qiiHSt_OzHtgpCBuO0uXf80uMvNY6P28Eoi2ougiIB8lSP28Q_l2haj8SBtlqOsa9_8vtIgiKSazk8HutgC-6": "KS004",
    "_a2S8_aq28_qa28q8aSR808PB8jhh2tH0iXt8gasvN0Y82fqo8Hkul8tHugha2ud_0H9a_8A2u0eOs89_PvCN_i728zIPvivjCvy": "KS005",
    "_a2S8_aq28_qa28qiavlagP_H8gFhHfY_uXfiluovN08iHuKoa-oiY8hSilYa2u7Y0Bz8Yip2f0ouXi0_iS3Ng8F2azZ8Sihgh-z": "KS006",
    "_a2S8_aq28_qa28q8uSSt_iIvulxh284guXn80aKvN0IO2uNoavzi0iJ2u_38HfHY0vh8_iR28gcus80luv2I_8x28oNi2fgghBY": "KS007",
    "_a2S8_aq28_qa28qii2za0uI-alxhvtDguXT8_auSNj8uHiOo8SJu0iM280euSat_0v0fgPWH80Lus8__avFIguuH8oIOHuTjh-z": "xiaoxia_2"

}

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
            msg = json_data.get("flag", "")
            if msg and str(msg) == "1":
                md5_id = json_data.get("md5", "")
                redis_handle = self.get_redis()
                redis_handle.lpush("pyq_ios", md5_id)
                time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                key = '_'.join(str(time_now).split())
                redis_handle.set("log:" + str(key), str(md5_id))
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
                    return {"msg": 'succes', "md5": md5_id, "flag": "1"}
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
        begin = request.GET.get('begin', "")
        end = request.GET.get('end', "")
        index = request.GET.get('index', "")
        size = request.GET.get('size', "")
        mediaUUID = request.GET.get("mediaUUID", "")
        if str(id) == "1":
            json_data = self.get_all_data(user)
            return JsonResponse(json_data, content_type="application/json", safe=True)
        elif str(id) == "2":
            json_data = self.get_rank(begin, end)
            return JsonResponse(json_data, content_type="application/json", safe=True)
        elif str(id) == "3":
            json_data = self.adRecordDetail(user, begin, end, index, size, mediaUUID)
            return JsonResponse(json_data, content_type="application/json", safe=True)
        elif str(id) == "4":
            json_data = self.get_baidu(user,begin,end)
            return JsonResponse(json_data, content_type="application/json", safe=True)

    def post(self, request):
        return JsonResponse({"msg": "errro request"})

    def get_baidu(self, user, begin, end):
        result = {}
        if user and user == '15210124311':
            tmp_list = []
            for dev_id, name in divce_id.items():
                amount = 0
                game_amount = 0
                app_amount = 0
                select_sql = "SELECT counts,game,app FROM material_baidu where device_id='{dev_id}' and `days` between '{A}' and '{B}'".format(
                    dev_id=dev_id, A=begin, B=end)
                result_data = self.select_data(select_sql)
                if result_data:
                    result_data = list(result_data)
                    for per in result_data:
                        tmp_dict = {}
                        per = list(per)
                        counts = per[0]
                        game = per[1]
                        app = per[2]
                        counts = int(counts)
                        game = int(game)
                        app = int(app)
                        amount += counts
                        game_amount += game
                        app_amount += app
                        tmp_dict["submitCount"] = amount
                        tmp_dict["game"] = game_amount
                        tmp_dict["app"] = app_amount
                        tmp_dict["phone"] = name
                        tmp_dict["mediaUUID"] = 4
                        tmp_list.append(tmp_dict)
            data = {}
            data["4"] = tmp_list
            result["stats"] = "0"
            result["msg"] = "成功"
            result["data"] = data
            return result

        else:
            result["stats"] = "4"
            result["msg"] = "该用户没有权限访问"
            result["data"] = []
            return result

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
                    mid = result[5]
                    if count:
                        count = int(count)
                    if str(mid) != "1":
                        sql_income = "SELECT counts FROM mediaInfo_day where account='{account}' and mediaUUID='{mid}'"
                        sql_income = sql_income.format(account=user, mid=str(mid))
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
            json_data["msg"] = "当前用户无数据！"
            json_data["data"] = tmp
        return json_data

    def get_rank(self, begin, end):
        result = {}
        data = {}
        tmp, account_list, defaultPrice = self.get_rank_pyq(begin, end)
        pyq_list = self.process_pyq(tmp, account_list, defaultPrice)
        ks = self.get_rank_ks(begin, end)
        ks_list = self.process_ks(ks, begin, end)
        gzh = self.get_rank_gzh(begin, end)
        gzh_list = self.process_gzh(gzh, begin, end)
        data["1"] = pyq_list
        data["3"] = ks_list
        data["2"] = gzh_list
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
                        account_dict[account] = value
                else:
                    if counts >= 40:
                        account_dict[account] = 1
                    else:
                        account_dict[account] = 0
        if account_dict:
            data = sorted(account_dict.items(), key=lambda x: x[1], reverse=True)
        return data

    def process_ks(self, ks, begin, end):
        ks_sum = "SELECT sum(counts) FROM mediaInfo_day where mediaUUID=3 and account='{phone}' and days BETWEEN '{A}' and '{B}'"
        sql_name = "SELECT realName FROM wechat_res where phone='{phone}'"
        ks_list = []
        if ks:
            for item in ks:
                ks_json = {}
                account = item[0]
                days = item[1]
                ks_result = self.ks_tj(account, begin, end)
                ks_sql = ks_sum.format(phone=account, A=begin, B=end)
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
                        name = name[0]
                        if name:
                            name = "**" + str(name[-1])
                        else:
                            name = ""
                    else:
                        name = ""
                if account and len(account) == 11:
                    account = str(account[0:3]) + "xxxx" + str(account[-3:])
                income = days * 10
                only = ""
                gather = ""
                all_ratio = ""
                if ks_result:
                    # print(ks_result)
                    only = ks_result.get("only", "")
                    gather = ks_result.get("gather", "")
                    all_ratio = ks_result.get("all_ratio", "")

                ks_json["phone"] = account
                ks_json["realName"] = name
                ks_json["income"] = income
                ks_json["submitCount"] = sum_count
                ks_json["vaildCount"] = gather
                ks_json["only"] = only
                ks_json["all_ratio"] = all_ratio
                ks_list.append(ks_json)
            if ks_list:
                ks_list = sorted(ks_list, key=lambda keys: keys['submitCount'], reverse=True)
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
            if pyq_list:
                pyq_list = sorted(pyq_list, key=lambda keys: keys['submitCount'], reverse=True)
            return pyq_list
        else:
            return []

    def get_rank_gzh(self, begin, end):
        gzh_account_dict = {}
        data = []
        sql = "SELECT account,counts FROM mediaInfo_day where mediaUUID=2 and days BETWEEN '{A}' and '{B}'"
        sql = sql.format(A=begin, B=end)
        result = self.select_data(sql)
        if result:
            result = list(result)
            for item in result:
                account = item[0]
                counts = item[1]
                value = gzh_account_dict.get(account, "")
                if counts:
                    counts = int(counts)
                if value:
                    if counts >= 40:
                        value += 1
                        gzh_account_dict[account] = value
                    else:
                        gzh_account_dict[account] = value
                else:
                    if counts >= 40:
                        gzh_account_dict[account] = 1
                    else:
                        gzh_account_dict[account] = 0
        if gzh_account_dict:
            data = sorted(gzh_account_dict.items(), key=lambda x: x[1], reverse=True)
        return data

    def process_gzh(self, gzh, begin, end):
        gzh_sum = "SELECT sum(counts) FROM mediaInfo_day where mediaUUID=2 and account='{phone}' and days BETWEEN '{A}' and '{B}'"
        sql_name = "SELECT realName FROM wechat_res where phone='{phone}'"
        gzh_list = []
        if gzh:
            # print(gzh)
            for item in gzh:
                gzh_json = {}
                account = item[0]
                days = item[1]
                gzh_sql = gzh_sum.format(phone=account, A=begin, B=end)
                sum_count = self.select_data(gzh_sql)
                if sum_count:
                    sum_count = list(sum_count)
                    sum_count = sum_count[0]
                    if sum_count:
                        sum_count = sum_count[0]
                        if sum_count:
                            sum_count = int(sum_count)
                        else:
                            sum_count = 0
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
                        name = name[0]
                        if name:
                            name = "**" + str(name[-1])
                        else:
                            name = ""
                    else:
                        name = ""
                if account and len(account) == 11:
                    account = str(account[0:3]) + "xxxx" + str(account[-3:])
                income = days * 10
                gzh_json["phone"] = account
                gzh_json["realName"] = name
                gzh_json["income"] = income
                gzh_json["submitCount"] = sum_count
                gzh_json["vaildCount"] = sum_count
                gzh_list.append(gzh_json)
            if gzh_list:
                gzh_list = sorted(gzh_list, key=lambda keys: keys['submitCount'], reverse=True)
            return gzh_list
        else:
            return []

    def adRecordDetail(self, user, begin, end, index, size, mediaUUID):
        final_json = {}

        if user and str(mediaUUID):
            result_list = []
            sql = "SELECT username,media_id,dt,buttom,nickname,lp,creative,appstore_link,sbType,images,ad_id,union_md5,insert_time,product FROM wechat_res  where phone='{user}' and  days BETWEEN '{begin}' and '{end}' ORDER BY days desc"
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

    def ks_tj(self, phone, begin, end):
        all_data_sql = "SELECT fp FROM ks_account_ext where `day` BETWEEN '%s' and '%s'" % (begin, end)
        all_data_tuple = self.select_data(all_data_sql)
        all_data = []
        if all_data_tuple:
            for item in list(all_data_tuple):
                all_data.append(item[0])
            len_data = len(list(all_data))
        else:
            len_data = 0
        cout_dict = {}
        if phone:
            tmp_list = []
            only = 0

            sql_amount = "SELECT fp FROM ks_account_ext where `day` BETWEEN '%s' and '%s' and phone='%s'" % (
                begin, end, phone)
            tmp_data_tuple = self.select_data(sql_amount)
            if tmp_data_tuple:
                for per in list(tmp_data_tuple):
                    tmp_list.append(per[0])
                len_tmp_data = len(list(tmp_list))
                if len_data:
                    all_ratio = round(len_tmp_data / len_data, 2)
                else:
                    all_ratio = 1
                cout_dict['all_ratio'] = all_ratio
                for t in list(tmp_list):
                    counts = all_data.count(t)
                    if counts == 1:
                        only += 1
                cout_dict["only"] = only
                cout_dict["gather"] = len_tmp_data
                cout_dict["game_ad_count"] = 0
                cout_dict["app_ad_count"] = 0
        return cout_dict

