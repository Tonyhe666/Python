
# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import thread
import time


class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        self.stories = []
        self.enable = False

    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            request = urllib2.Request(url,headers=self.headers)
            response = urllib2.urlopen(request)
            pageCode = response.read().decode('utf-8')
            return  pageCode
        except urllib2.URLError,e:
            if hasattr(e,'code'):
                print e.code
            if hasattr(e,'reason'):
                print e.reason
            return None

    def getPageItem(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            return None
        pattern = re.compile('<div.*?content">.*?<span>(.*?)</span>.*?</div>(.*?)',re.S)
        items = re.findall(pattern, pageCode)
        pageStores = []
        for item in items:
            replaceBr = re.compile('<br/>')
            text = re.sub(replaceBr,"\n",item[0])
            pageStores.append(text)
            #print item[0]
        return pageStores

    def loadPage(self):
        if self.enable == True:
            pageStories = self.getPageItem(self.pageIndex)
            if pageStories:
                self.stories.append(pageStories)
                self.pageIndex += 1

    def getOneStory(self,pageStories,page):
        for story in pageStories:
            input = raw_input()
            if input == "Q":
                self.enable = False
                return
            print u"第%d页 %s" %(page, story)

    def start(self):
        print u"正在抓去糗事百科，按回车查看新段，Q退出"
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



