
# -*- coding:utf-8 -*-
import urllib
import requests
import re
import time


class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []
        self.enable = False

    def getPage(self, pageIndex):
        url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
        pageCode = requests.get(url, headers=self.headers)
        return pageCode

    def getPageItem(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            return None
        pattern = re.compile('<div.*?content">.*?<span>(.*?)</span>.*?</div>.*?<span.*?vote">.*?number">(.*?)</i>',re.S)
        items = re.findall(pattern, pageCode)
        pageStores = []
        for item in items:
            replaceBr = re.compile('<br/>')
            text = re.sub(replaceBr,"\n",item[0])
            pageStores.append([item[1],text.strip()])
        return pageStores

    def loadPage(self):
        if self.enable == True:
            pageStories = self.getPageItem(self.pageIndex)
            if pageStories:
                self.stories.append(pageStories)
                self.pageIndex += 1

    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input = input()
            if input == "Q":
                self.enable = False
                return
            print( u"第%d页\n赞:%s\n%s" %(page, story[0], story[1]))

    def start(self):
        print( u"正在抓去糗事百科，按回车查看新段子，Q退出")
        self.enable = True
        nowPage = 0
        while self.enable:
            if len(self.stories)>0:
                pageStories = self.stories[0]
                nowPage += 1
                del self.stories[0]
                self.getOneStory(pageStories, nowPage)
            else:
                self.loadPage()

spider = QSBK()
spider.start()



