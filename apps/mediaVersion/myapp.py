#!/usr/bin/env python
# encoding: utf-8
import redis
import requests
from datetime import datetime
from pyquery import PyQuery as pq
import pymysql
from DBUtils.PooledDB import PooledDB

media_pkg = {
    '360浏览器': 'com.qihoo.browser',
    'hao123': '',
    'IT之家': 'com.ruanmei.ithome',
    'pptv com.pplive.androidphone': '',
    'QQ浏览器': 'com.tencent.mtt',
    'QQ空间': 'com.qzone',
    'TapTap': 'com.taptap',
    'UC头条': 'com.uc.infoflow',
    'UC浏览器': 'com.UCMobile',
    'vivo浏览器': 'com.vivo.browser',
    'wifi万能钥匙': 'com.snda.wifilocating',
    'zaker': 'com.myzaker.ZAKER_Phone',
    '一点资讯': 'com.hipu.yidian',
    '东方头条': 'com.songheng.eastnews',
    '中关村在线': 'com.zol.android',
    '中华万年历': 'cn.etouch.ecalendar',
    '中央天气预报': 'com.nineton.weatherforecast',
    '乐视视频': 'com.letv.android.client',
    '今日十大热点': 'com.sogou.toptennews',
    '今日头条': 'com.ss.android.article.news',
    '今日影视大全': 'cn.quicktv.androidpro',
    '今日要看': '',
    '优酷视频': 'com.youku.phone',
    '凤凰新闻': 'com.ifeng.news2',
    '凤凰视频': 'com.ifeng.newvideo',
    '华为浏览器': '',
    '咪咕影院': 'com.cmvideo.migumovie',
    '哔哩哔哩': 'tv.danmaku.bili',
    '唔哩头条': 'com.caishi.cronus',
    '土豆视频': 'com.tudou.android',
    '墨迹天气': 'com.moji.mjweather',
    '天天快报': 'com.tencent.reading',
    '好奇心日报': '',
    # '好看视频': 'com.baidu.haokan',
    '小米浏览器': '',
    '小米画报': '',
    '小米视频': 'com.miui.video',
    '引力资讯': '',
    '微信': 'com.tencent.mm',
    '快手': 'com.smile.gifmaker',
    '悦头条': 'com.expflow.reading',
    '懂球帝': 'com.dongqiudi.news',
    '抖音': 'com.ss.android.ugc.aweme',
    '搜狐新闻': 'com.sohu.newsclient',
    '搜狐视频': 'com.sohu.sohuvideo',
    '搜狗搜索': 'com.sogou.activity.src',
    '搜狗浏览器 ': 'sogou.mobile.explorer',
    '斗鱼': 'air.tv.douyu.android',
    '新浪体育': 'cn.com.sina.sports',
    '新浪微博': 'com.sina.weibo',
    '新浪新闻': 'com.sina.news',
    '新浪财经': 'cn.com.sina.finance',
    '最右': 'cn.xiaochuankeji.tieba',
    '段友': '',
    '汽车之家': 'com.cubic.autohome',
    '波波视频': 'tv.yixia.bobo',
    '火山小视频': 'com.ss.android.ugc.live',
    '爱奇艺视频': 'com.qiyi.video',
    '爱看': '',
    '猎豹浏览器': 'com.ijinshan.browser_fast',
    '猎豹清理大师': 'com.cleanmaster.mguard_cn',
    '球球视频': '',
    '界面新闻': 'com.jiemian.news',
    '百度': 'com.baidu.searchbox',
    '百度浏览器': 'com.baidu.browser.apps',
    '百度视频': 'com.baidu.video',
    '百度贴吧': 'com.baidu.tieba',
    '皮皮搞笑': '',
    '皮皮虾': 'com.sup.android.superb',
    '知乎': 'com.zhihu.android',
    '米尔军事': 'com.miercnnew.app',
    '糗事百科': 'qsbk.app',
    '网易新闻': 'com.netease.newsreader.activity',
    '腾讯QQ': 'com.tencent.mobileqq',
    '腾讯新闻': 'com.tencent.news',
    '腾讯视频': 'com.tencent.qqlive',
    '虎扑': 'com.hupu.games',
    '西瓜视频': 'com.ss.android.article.video',
    '豆瓣': 'com.douban.frodo',
    '趣头条': 'com.jifen.qukan',
    '遨游浏览器': 'com.mx.browser',
    '风行视频': 'com.funshion.video.mobile',
    '车来了': 'com.ygkj.chelaile.standard',
    '手机迅雷': 'com.xunlei.downloadprovider',
    '全民小视频': 'com.baidu.minivideo',
}
pool1 = PooledDB(pymysql, 10, host='192.168.168.83', port=3306, user='root',
                 password='Adi_mysql',
                 database='adi', charset='utf8')


class MyAPP(object):
    def __init__(self):
        self.url = "https://android.myapp.com/myapp/detail.htm?apkName={}"
        self.headers = {
            'Content-Encoding': 'gzip',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36',
        }
        self.zh2en = {
            u'版本号：': 'version',
            u'更新时间：': 'update_time',
            u'开发商：': 'company',
        }

    @staticmethod
    def _list2dict(list_data):
        i = iter(list_data)
        d = dict(zip(i, i))
        return d

    def get_data_from_apk_name(self, pkg):
        url = self.url.format(pkg)
        return self.get_data_from_url(url)

    def get_data_from_url(self, url):
        try:
            r = requests.get(url=url, headers=self.headers)
            if r.status_code == 200:
                result = self.process_res(r.text)
                return result
        except Exception as e:
            print(e)

    def process_res(self, content):
        # data = {}
        # media_version = ""
        # company = ""
        # update_time = ""

        _pq = pq(content)
        main_container = _pq(".det-main-container")

        app_info = main_container(".det-ins-container")
        icon_url = app_info(".det-icon img").attr("src")
        product = app_info(".det-ins-data .det-name .det-name-int").text()
        genre = app_info("#J_DetCate").text()

        app_info = main_container(".det-othinfo-container")
        oth_info = []
        for div in app_info.children().items():
            info = div.text()
            oth_info.append(self.zh2en.get(info) or info)
            if len(oth_info) >= 6:
                break
        oth_info = self._list2dict(oth_info)
        update_time = app_info("#J_ApkPublishTime").attr("data-apkpublishtime")
        if update_time:
            try:
                oth_info['update_time'] = datetime.fromtimestamp(int(update_time)).strftime('%Y-%m-%d %H:%M:%S')
            except Exception as e:
                print("更新时间有误：", e)

        app_info = {
            "icon_url": icon_url,
            "product": product,
            "genre": genre,
        }
        app_info.update(oth_info)
        return app_info

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
    rdp_local = redis.ConnectionPool(host='127.0.0.1', port=6379, db=2)
    rdc_local = redis.StrictRedis(connection_pool=rdp_local)
    cm = MyAPP()
    # print(cm.get_data_from_apk_name("cn.xiaochuankeji.zuiyouLite"))
    for media, pkg in media_pkg.items():
        if pkg:
            result_dict = cm.get_data_from_apk_name(pkg)
            if result_dict:
                icon_url = result_dict.get("icon_url", "")
                product = result_dict.get("product", "")
                genre = result_dict.get("genre", "")
                version = result_dict.get("version", "")
                release_time = result_dict.get("update_time", "")
                company = result_dict.get("company", "")

                old_version = rdc_local.get("myapp:" + pkg)
                if not old_version:
                    rdc_local.set("myapp:" + pkg, version)
                    insert_sql = "insert into myapp(icon_url,`name`,genre,version,release_time,company,apk_name) values(%s,%s,%s,%s,%s,%s,%s)"
                    param = [icon_url, product, genre, version, release_time, company, pkg]
                    insert_result = cm.insert(insert_sql, param)
                    if insert_result:
                        print(media + "插入成功--andriod！")
                else:
                    old_version = bytes.decode(old_version)
                    if str(old_version) != str(version):
                        print(str(old_version))
                        print(str(version))
                        update_sql = "UPDATE myapp set version='{version}',release_time='{release_time}',update_time=NOW() where apk_name='{pkg}'"
                        update_sql = update_sql.format(version=version, release_time=release_time, pkg=pkg)
                        update_result = cm.excute_local(update_sql)
                        if update_result:
                            print(media + "更新成功--andriod！")
                    else:
                        print(media + "暂无更新--andriod！")
