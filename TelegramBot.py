# !/usr/bin/python
# _*_ coding:utf-8 _*_

import telebot
import logging
from telebot import apihelper
import requests
from bs4 import BeautifulSoup
import time

TOKEN = 'XXXXX'
bot = telebot.TeleBot(TOKEN)
apihelper.proxy = {'http': 'http://127.0.0.1:1087', 'https': 'http://127.0.0.1:1087'}
logger = telebot.logger
telebot.logger.setLevel(logging.ERROR)
commonds = ['start', 'weather','m2', 'eos']

def get_weather():
    resp = requests.get('http://t.weather.sojson.com/api/weather/city/101010100')
    strjson = resp.json()
    if strjson["status"] == 200 :
        today = strjson["data"]["forecast"][0]
        msg = u"今天是%s\n%s\n%s\n%s/%s\n%s:%s\npm2.5:%d\n%s\n" % (today['ymd'], today['week'], today['type'], today['high'], today['low'], today['fx'], today['fl'],strjson["data"]['pm25'], today['notice'])
        return msg
    else:
        return u'服务异常 http错误码：%d' % strjson["status"]

def get_eos():
    resp = requests.get('https://www.feixiaohao.com/currencies/eos/')
    if resp.status_code == 200:
        soup_text = BeautifulSoup(resp.text, 'html.parser')
        mainPrice = soup_text.find_all('div', class_='mainPrice')
        str = mainPrice[0].text.replace('\n', '').replace(' ', '')
        lowHeigt = soup_text.find_all('div',class_='lowHeigt')
        str1 = lowHeigt[0].text.replace('\n', '').replace('  ', '')
        return u'EOS价格：%s\n%s' % (str, str1)
    else:
        return  u'服务异常 http错误码：%d' % resp.status_code

def get_m2():
    url = 'http://xx.xx.xx.xx:19081'
    param = {'username': '***', 'password':'0000'}
    #headers = {'Host': '101.37.12.15:19081','User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'}
    rs = requests.session()
    resp = rs.post(url + '/adminUserAuthentication.lc',data=param)
    if resp.status_code == 200:
        param = {'startTime': '', 'endTime': '', 'orderNO':'', 'playerID':0,'payType':'','productType':''}
        orderlist = rs.post(url + '/manage_pay_order.do', data=param)
        if orderlist.status_code == 200 :
            order = orderlist.json()
            ret = ''
            i = 0
            for pay in order['data']:
                if i > 3:
                    break
                i = i + 1
                ret = ret + u'{0} 订单数: {1} 金额: {2} 独立用户: {3}\n'.format( pay['day'], pay['order_count'], pay['totalpay'], pay['players'])
            return ret
        else:
            return u'服务异常 http错误码：%d' % resp.status_code
    else:
        return u'服务异常 http错误码：%d' % resp.status_code

def get_m2_report():
    pass

@bot.message_handler(commands=commonds)
def send_welcome(message):
    hello = u'Hi %s:\n' % message.from_user.first_name
    if message.content_type == u'text' and message.text == u'/start' :
        bot.reply_to(message, hello + u'我是一个电报机器人, 可以快速的帮你做一些事情 你可以试试一下命令 /eos  /m2  /weather')
        pass
    elif message.content_type == u'text' and message.text == u'/weather' :
        bot.reply_to(message, hello + get_weather())
        pass
    elif message.content_type == u'text' and message.text == u'/m2':
        bot.reply_to(message, hello + get_m2())
        pass
    elif message.content_type == u'text' and message.text == u'/eos':
        bot.reply_to(message, hello + get_eos())
        pass
    #bot.delete_message(message.chat.id, message.message_id)

try:
    bot.polling(none_stop=True, interval=0, timeout=120)
except requests.exceptions.ConnectionError,e:
    print(u'链接错误')
    time.sleep(3)
    bot.infinity_polling()
except requests.exceptions.ConnectTimeout,e:
    print(u'链接超时')
    time.sleep(3)
    bot.infinity_polling()
except requests.exceptions.ReadTimeout,e:
    print(u'读取超时')
    time.sleep(3)
    bot.infinity_polling()