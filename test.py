#_*_ coding: utf-8 _*_

import urllib2
import cookielib

# save cookie
# filename = "cookie.txt"
# cookie = cookielib.MozillaCookieJar(filename)
# handler = urllib2.HTTPCookieProcessor(cookie)
# opener = urllib2.build_opener(handler)
# response = opener.open("http://www.baidu.com")
# for item in cookie:
#     print "Name = " + item.name
#     print "vale = " + item.value
# cookie.save(ignore_discard=True, ignore_expires=True)

# load cookie

# filename = "cookie.txt"
# cookie = cookielib.MozillaCookieJar()
# cookie.load(filename,ignore_discard=True, ignore_expires=True)
# req = urllib2.Request("http://www.baidu.com")
# handler = urllib2.HTTPCookieProcessor(cookie)
# opener = urllib2.build_opener(handler)
# response = opener.open(req)
# print response.read()

# regex

import re
# pattern = re.compile("hello")
#
# result1 = re.match(pattern,'hello')
# result2 = re.match(pattern, "helloo hl")
# result3 = re.match(pattern, "helo hl")
# result4 = re.match(pattern, 'hello hl')
#
# if result1:
#     print result1.group()
# else:
#     print "1匹配失败"
#
# if result2:
#     print  result2.group()
# else:
#     print "2匹配失败"
#
# if result3:
#     print result3.group()
# else:
#     print "3匹配失败"
#
# if result4:
#     print result4.group()
# else:
#     print "4匹配失败"


page = 1
url = 'http://www.qiushibaike.com/hot/page/' + str(page)
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }
try:
    request = urllib2.Request(url,headers = headers)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
    pattern = re.compile('<div .*?author clearfix".*?<img src=(.*?)alt=(.*?)>.*?<div.*?content">.*?<span>(.*?)</span>.*?</div>.*?<div class="stats.*?class="number">(.*?)</i>',re.S)
    items = re.findall(pattern,content)
    for item in items:
        print item[0],item[1],item[2],item[3]
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason

