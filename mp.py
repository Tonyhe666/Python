# _*_ coding:utf-8 _*_

import urllib
import requests
import re
import os
from bs4 import BeautifulSoup
import json


def callbackfunc(blocknum,blockSize, totalSize):
    percent = 100*blocknum*blockSize/totalSize
    if percent == 100:
        print( u'###当前大小：%02f, 总大小：%02f,****%.2f%% ###' %( blocknum*blockSize, totalSize, percent))

def download(url,name):
    path = '../bsj/' + name + '.mp4'
    urllib.urlretrieve(url, path, callbackfunc)

#download('https://mov.bn.netease.com/open-movie/nos/flv/2015/01/19/SAFD842HJ_sd.flv')

def print_dic(dic):
    for k,v in dic.items():
        print(k,v)

def print_list(list):
    for i in list:
        if type(i) == type({}):
            print_dic(i)
        else:
            print(i)


def gethtml(page):
    html = requests.get('http://www.budejie.com/video/'+str(page))
    task_list = []
    # pattern = re.compile(r'<div.*?j-video-c".*?data-title=(.*?)data-date=(.*?)data-time=(.*?)data-videoMlen.*?data-mp4=(.*?)>.*?</div>',re.S)
    # div_vedio_list = re.findall(pattern, html.text)
    # for div_vedio in div_vedio_list:
    #     task = {}
    #     task["title"] = div_vedio[0].strip()
    #     task["date"] = div_vedio[1].strip()
    #     task["time"] = div_vedio[2].strip()
    #     task["url"] = div_vedio[3]
    #     task["fmt"] = div_vedio[3][-5:-1]
    #     print task["title"], task["url"], task["fmt"], task["date"], task["time"]
    #     task_list.append(task)

    html_soup = BeautifulSoup(html.text, 'lxml')
    div_video_list = html_soup.find_all('div', class_='j-video-c')
    for div_video in div_video_list:
        # print div_video['data-title'], div_video['data-date'], div_video['data-time']
        id = 'j-v-' + div_video['data-id']
        video = div_video.find('div', id=id)
        if video:
            # print video['data-mp4']
            task = {'title': div_video['data-title'][0:-3],
                    'date': div_video['data-date'],
                    'time': div_video['data-time'],
                    'url': video['data-mp4']}
            # print_dic(task)
            task_list.append(task)
    return  task_list


# os.makedirs(os.path.join('../', 'bsj'))
# os.chdir(os.path.join('../', 'bsj'))
# for page in range(2,10):
#     task_list = gethtml(page)
#     print u"开始下载第%d页..." % page
#     for task in task_list:
#         print_dic(task)
#         download(task['url'], task['title'])
#     print u"第%d页下载完成..." % page


#download('https://aweme.snssdk.com/aweme/v1/playwm/?video_id=4b211f766e344c6da3445cad151676bf&line=0','test' )

URL= r'https://api.amemv.com/aweme/v1/discover/search/?iid=24607383639&device_id=34943414774&os_api=18&app_name=aweme&channel=App%20Store&idfa=454C6328-7459-4C2B-93E8-3B97C9E02E9D&device_platform=iphone&build_number=17201&vid=73922B00-896C-4178-AFDE-A6DE7E25C53C&openudid=22076ed81b3351e95149983f2dcf3a6de53c7c7d&device_type=iPhone9,2&app_version=1.7.2&version_code=1.7.2&os_version=11.2.1&screen_width=1242&aid=1128&ac=WIFI&count=20&cursor=0'\
     +'&keyword=%s&search_source=discover&type=1&as=a175f08950b2ea5826&ts=1519781920' % '56067282'
res = requests.get(URL)
print( res.text)
json.loads(res.text)
