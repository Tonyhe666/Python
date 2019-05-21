# !/usr/bin/python
# _*_ coding:utf-8 _*_

import requests
import time
import urllib
import os

class DouYin():
    def __init__(self):
        """ 根据用户分享后的uid抓去抖音视频，并下载 """
        self.task = []

    def search(self, user_id):
        #这个方法服务器有校验，不好使。换id后不好使
        # print '获取用户信息'
        url = 'https://api.amemv.com/aweme/v1/discover/search/?iid=24607383639&device_id=34943414774&os_api=18&app_name=aweme&channel=App%20Store&idfa=454C6328-7459-4C2B-93E8-3B97C9E02E9D&device_platform=iphone&build_number=17201&vid=73922B00-896C-4178-AFDE-A6DE7E25C53C&openudid=22076ed81b3351e95149983f2dcf3a6de53c7c7d&device_type=iPhone9,2&app_version=1.7.2&version_code=1.7.2&os_version=11.2.1&screen_width=1242&aid=1128&ac=WIFI&count=20&cursor=0'+\
              '&keyword=%s0&search_source=discover&type=1&as=a115267905742afff6&ts=1519808325' % user_id
        ret = requests.get(url)
        strjson = ret.json()
        # print strjson
        user_info = strjson['user_list'][0]['user_info']
        # print user_info['short_id'] #抖音id
        # print user_info['birthday']
        # print user_info['nickname']
        # print user_info['aweme_count']
        # print user_info['favoriting_count']
        # print user_info['uid']
        # print 'https://www.douyin.com/share/user/%s' % user_info['uid']
        return user_info

    def postVedio(self, uid, count):
        html = requests.get('https://www.douyin.com/aweme/v1/aweme/post/?user_id=%s&count=%d' %(uid, count))
        strjson = html.json()
        # print  '获取自己发的视频 %d' % len(strjson['aweme_list'])
        for i in strjson['aweme_list']:
            task = {}
            task['url'] = i['video']['play_addr']['url_list'][0]
            task['uri'] = i['video']['play_addr']['uri']
            self.task.append(task)

    def favoriteVedio(self, uid, count):
        html = requests.get('https://www.douyin.com/aweme/v1/aweme/favorite/?user_id=%s&count=%d' %(uid, count))
        strjson = html.json()
        # print  '获取喜欢的视频 %d' % len(strjson['aweme_list'])
        # print len(strjson['aweme_list'])
        for i in strjson['aweme_list']:
            task = {}
            task['url'] = i['video']['play_addr']['url_list'][0]
            task['uri'] = i['video']['play_addr']['uri']
            self.task.append(task)

    def callbackfunc(self,blocknum, blockSize, totalSize):
        percent = 100 * blocknum * blockSize / totalSize
        if percent == 100:
            print( u'###当前大小：%02f, 总大小：%02f,****%.2f%% ###' % (blocknum * blockSize, totalSize, percent))

    def download(self,url, name):
        path = './' + name + '.mp4'
        is_file_exist = os.path.isfile(path)
        if is_file_exist:
            # print name + u"存在，返回"
            return
        urllib.urlretrieve(url, path, self.callbackfunc)

    def downloadAll(self):
        for task in self.task:
            self.download(task['url'],task['uri'])

    def makeDir(self, name):
        path = os.path.join('../Douyin', name)
        is_exist = os.path.exists(path)
        if not is_exist:
            os.makedirs(path)
            os.chdir(path)
            pass
        else:
            os.chdir(path)
            pass

    def test(self):
        html = requests.get('https://www.douyin.com/aweme/v1/aweme/post/?user_id=64790405854')
        print( html.json())


#'https://www.douyin.com/share/user/64790405854'
#分享后拿到用户uid，这个不是抖音号
Spider = DouYin()
short_id = input(u'请输入用户uid：')
Spider.postVedio(short_id, 10000)
Spider.favoriteVedio(short_id, 10000)
Spider.makeDir(short_id) # 以抖音id命名
Spider.downloadAll()



