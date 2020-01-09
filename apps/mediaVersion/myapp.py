#!/usr/bin/env python
# encoding: utf-8

import requests
from datetime import datetime
from pyquery import PyQuery as pq

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
    'vivo浏览器': '',
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
    '好看视频': 'com.baidu.haokan',
    '小米浏览器': '',
    '小米画报': '',
    '小米视频': 'com.miui.video',
    '引力资讯': '',
    '微信-公众号': 'com.tencent.mm',
    '微信-小程序': 'com.tencent.mm',
    '微信-朋友圈': 'com.tencent.mm',
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
    '猎豹浏览器': '',
    '猎豹清理大师': 'com.cleanmaster.mguard_cn',
    '球球视频': '',
    '界面新闻': 'com.jiemian.news',
    '百度': 'com.baidu.searchbox',
    '百度浏览器': 'com.baidu.browser.apps',
    '百度视频': 'com.baidu.video',
    '百度贴吧': 'com.baidu.tieba',
    '皮皮搞笑': 'cn.xiaochuankeji.zuiyouLite',
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
}


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
            oth_info['update_time'] = datetime.fromtimestamp(int(update_time)).strftime('%Y-%m-%d %H:%M:%S')

        app_info = {
            "icon_url": icon_url,
            "product": product,
            "genre": genre,
        }
        app_info.update(oth_info)
        return app_info


if __name__ == '__main__':
    cm = MyAPP()
    print(cm.get_data_from_apk_name('com.tencent.mobileqq'))
