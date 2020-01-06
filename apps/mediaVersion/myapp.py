#!/usr/bin/env python
# encoding: utf-8

import requests
from datetime import datetime
from pyquery import PyQuery as pq


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
            print (e)

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
    print (cm.get_data_from_apk_name('com.tencent.mobileqq'))
