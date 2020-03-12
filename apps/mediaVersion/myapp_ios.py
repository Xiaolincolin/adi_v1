#!/usr/bin/env python
# encoding: utf-8
import redis
import requests
import datetime
import pymysql
from DBUtils.PooledDB import PooledDB

pool1 = PooledDB(pymysql, 10, host='192.168.168.83', port=3306, user='root',
                 password='Adi_mysql',
                 database='adi', charset='utf8')
media_appid = {
    '360浏览器': '892311054',
    'hao123': '506298503',
    'IT之家': '570610859',
    'pptv': '438426078',
    'QQ浏览器': '370139302',
    'QQ空间': '364183992',
    'TapTap': '1444595166',
    'UC头条': '1085421653',
    'UC浏览器': '586871187',
    'vivo浏览器': '',
    'wifi万能钥匙': '919854496',
    'zaker': '462149227',
    '一点资讯': '976039116',
    '东方头条': '1030220577',
    '中关村在线': '539824445',
    '中华万年历': '494776019',
    '中央天气预报': '455611831',
    '乐视视频': '385285922',
    '今日十大热点': '1256338755',
    '今日头条': '529092160',
    '今日影视大全': '1020114152',
    '今日要看': '',
    '优酷视频': '336141475',
    '凤凰新闻': '395133418',
    '凤凰视频': '376343878',
    '华为浏览器': '',
    '咪咕影院': '1029829434',
    '哔哩哔哩': '736536022',
    '唔哩头条': '1068045574',
    '土豆视频': '395898626',
    '墨迹天气': '434209233',
    '看点快报': '996866372',
    '好奇心日报': '',
    '好看视频': '1498891869',
    '小米浏览器': '',
    '小米画报': '',
    '小米视频': '',
    '引力资讯': '',
    '微信': '414478124',
    '快手': '440948110',
    '悦头条': '1454934409',
    '懂球帝': '766695512',
    '抖音': '1142110895',
    '搜狐新闻': '436957087',
    '搜狐视频': '458587755',
    '搜狗搜索': '891230263',
    '搜狗浏览器': '548608066',
    '斗鱼': '863882795',
    '新浪体育': '564760110',
    '新浪微博': '350962117',
    '新浪新闻': '299853944',
    '新浪财经': '430165157',
    '最右': '942443472',
    '段友': '',
    '汽车之家': '385919493',
    '波波视频': '',
    '火山小视频': '1086047750',
    '爱奇艺视频': '445375097',
    '爱看': '1168490851',
    '猎豹浏览器': '',
    '猎豹清理大师': '',
    '球球视频': '',
    '界面新闻': '930342070',
    '百度': '382201985',
    '百度浏览器': '789634484',
    '百度视频': '588287777',
    '百度贴吧': '477927812',
    '皮皮搞笑': '',
    '皮皮虾': '1393912676',
    '知乎': '432274380',
    '米尔军事': '598835215',
    '糗事百科': '422853458',
    '网易新闻': '425349261',
    '腾讯QQ': '399363156',
    '腾讯新闻': '444934666',
    '腾讯视频': '458318329',
    '虎扑': '906632439',
    '西瓜视频': '1134496215',
    '豆瓣': '907002334',
    '趣头条': '1113268900',
    '遨游浏览器': '541052011',
    '风行视频': '1028313528',
    '车来了': '667831823',
    '手机迅雷': '',
    '全民小视频': '1329385145',
    '芒果TV': '629774477'
}


class MyappIos:
    def get_appstore(self, appid):

        url = 'https://itunes.apple.com/cn/app/id{}?mt=8'.format(appid)
        headers = {
            'Accept-Language': 'zh-Hans-CN',
            'User-Agent': 'AppStore/2.0 iOS/10.0.2 model/iPhone7,2 hwp/t7000 build/14A456 (6; dt:106)',
            'X-Apple-Connection-Type': 'WiFi',
            'X-Apple-Store-Front': '143465-19,29',
        }
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            try:
                j = r.json()
                if j:
                    version_history = j['pageData']['versionHistory']
                    release_date = version_history[0]['releaseDate']
                    version_string = version_history[0]['versionString']
                    _id = j['pageData']['id']
                    results = j['storePlatformData']['product-dv']['results'][_id]
                    artwork_url = results['artwork']['url'].replace('{w}x{h}bb.{f}', '100x0w.jpg')
                    bundle_id = results['bundleId']
                    genre_names = results['genreNames']
                    name = results['name']
                    name_raw = results['nameRaw']
                    support_url = results['softwareInfo']['supportUrl']
                    artist_id = results['artistId']
                    artist_name = results['artistName']

                    type_id = 1 if genre_names[0] == u'游戏' else 2
                    utctime = datetime.datetime.strptime(release_date, '%Y-%m-%dT%H:%M:%SZ')
                    localtime = utctime + datetime.timedelta(hours=8)
                    res = {
                        'typeId': type_id,
                        'releaseDate': localtime.strftime("%Y-%m-%d %H:%M:%S"),
                        'releaseVer': version_string,
                        'iconUrl': artwork_url,
                        'bundleId': bundle_id,
                        "genreNames": '/'.join(genre_names),
                        "name": name.split('-')[0],
                        "nameRaw": name_raw,
                        "supportUrl": support_url,
                        "artistId": artist_id,
                        "artistName": artist_name,
                    }
                    return res
            except Exception as e:
                print(e)

    def insert(self, sql, param):
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
    rdp_local = redis.ConnectionPool(host='127.0.0.1', port=6379, db=2)  # 默认db=0，测试使用db=1
    rdc_local = redis.StrictRedis(connection_pool=rdp_local)
    myappios = MyappIos()
    for media, appid in media_appid.items():
        if appid:
            apps = myappios.get_appstore(appid)
            if apps:
                typeId = apps.get("typeId", "")
                releaseDate = apps.get("releaseDate", "")
                releaseVer = apps.get("releaseVer", "")
                iconUrl = apps.get("iconUrl", "")
                bundleId = apps.get("bundleId", "")
                genreNames = apps.get("genreNames", "")
                name = apps.get("name", "")
                nameRaw = apps.get("nameRaw", "")
                supportUrl = apps.get("supportUrl", "")
                artistId = apps.get("artistId", "")
                artistName = apps.get("artistName", "")
                old_version = rdc_local.get("myappios:" + str(appid))
                if not old_version:
                    rdc_local.set("myappios:" + str(appid), releaseVer)
                    insert_sql = "insert into myapp_ios(icon_url,type_id,`name`,genre,release_time,version,apk_name,supportUrl,company,appid) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                    param = [iconUrl, typeId, name, genreNames, releaseDate, releaseVer, bundleId, supportUrl,
                             artistName, appid]
                    insert_result = myappios.insert(insert_sql, param)
                    if insert_result:
                        print(media + "插入成功！")
                else:
                    old_version = bytes.decode(old_version)
                    if str(old_version) != str(releaseVer):
                        print(str(old_version))
                        print(str(releaseVer))
                        update_sql = "UPDATE myapp_ios set version='{version}',release_time='{releaseDate}',update_time=NOW() where appid='{appid}'"
                        update_sql = update_sql.format(version=releaseVer, releaseDate=releaseDate, appid=appid)
                        update_result = myappios.excute_local(update_sql)
                        if update_result:
                            print(media + "更新成功！")
                    else:
                        print(media + "暂无更新--ios")
