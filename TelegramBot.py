# !/usr/bin/python
# _*_ coding:utf-8 _*_
import telebot
import requests
from bs4 import BeautifulSoup
import time
import yaml
from flask_restful import Resource,Api
import flask

f =open('config.yaml')
if f == None:
    print('缺少配置文件')
    exit(0)
config = yaml.safe_load(f)

bot = telebot.TeleBot(config['TOKEN'])
commonds = ['start', 'm2', 'eos', 'weather']

def get_weather():
    try:
        headers = {
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
            'Host':'t.weather.sojson.com',
            'Accept-Encoding':'gzip, deflate',
            'Connection':'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests':1,
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3'}
        resp = requests.get('http://t.weather.sojson.com/api/weather/city/101010100',headers=headers)
        resp.raise_for_status()
        strjson = resp.json()
        data = strjson["data"]
        forcast = data['forecast']
        today = forcast[0]
        tomorrow = forcast[1]
        after_tomorrow = forcast[2]
        msg = u'当前：{0} 温度：{1} pm25：{2} 湿度：{3}\n'.format(data['quality'],data['wendu'],data['pm25'],data['shidu'])
        msg = msg + u'今天：{0} {1} {2}:{3} {4}\n'.format(today['type'], today['high'], today['low'],today['fx'], today['fl'])
        msg = msg + u'明天：{0} {1} {2}:{3} {4}\n'.format(tomorrow['type'],tomorrow['high'],tomorrow['low'],tomorrow['fx'],tomorrow['fl'])
        msg = msg + u'后天：{0} {1} {2}:{3} {4}\n'.format(after_tomorrow['type'],after_tomorrow['high'],after_tomorrow['low'],after_tomorrow['fx'],after_tomorrow['fl'])
        msg = msg + today['notice']
        return msg
    except:
        return u'天气服务异常'

def get_eos():
    try:
        resp = requests.get('https://www.feixiaohao.com/currencies/eos/')
        resp.raise_for_status()
        soup_text = BeautifulSoup(resp.text, 'html.parser')
        mainPrice = soup_text.find_all('div', class_='mainPrice')
        str = mainPrice[0].text.replace('\n', '').replace(' ', '')
        lowHeigt = soup_text.find_all('div',class_='lowHeigt')
        str1 = lowHeigt[0].text.replace('\n', '').replace('  ', '')
        return u'EOS价格：%s\n%s' % (str, str1)
    except:
        return u'服务异常'

def get_m2():
    url = config['M2GMURL']
    param = {'username': config['NAME'], 'password':config['PASSWORD']}
    rs = requests.session()
    try:
        resp = rs.post(url + '/adminUserAuthentication.lc',data=param)
        resp.raise_for_status()
        # 获取订单
        param = {'startTime': '', 'endTime': '', 'orderNO':'', 'playerID':0,'payType':'','productType':''}
        orderlist = rs.post(url + '/manage_pay_order.do', data=param)
        ret = ''
        orderlist.raise_for_status()
        if orderlist.status_code == 200 :
            order = orderlist.json()
            i = 0
            for pay in order['data']:
                if i > 3:
                    break
                i = i + 1
                ret = ret + u'`{0} 订单数：{1} 金额：{2} 独立用户：{3}`\n'.format( pay['day'], pay['order_count'], pay['totalpay'], pay['players'])
        else:
            ret =  u'获取订单服务异常 http错误码：%d' % resp.status_code

        # 获取每日统计
        dashboard = rs.post(url + '/dashboard.lc')
        ret = ret + '\n'
        dashboard.raise_for_status()
        soup_text = BeautifulSoup(dashboard.text, 'html.parser')
        data = soup_text.find_all('tr', class_='text-c')
        i = 0
        for a in data:
            if i == 0:
                i = i + 1
                continue
            if i > 3:
                break
            td = a.find_all('td')
            i = i + 1
            date = td[0].text.replace('\n', '').replace(' ', '')
            new_add = td[2].text.replace('\n', '').replace(' ', '')
            card = td[13].text.replace('\n', '').replace(' ', '')
            login = td[14].text.replace('\n', '').replace(' ', '')
            dau = td[15].text.replace('\n', '').replace(' ', '')
            ret = ret + u'`{0} 新增：{1} 耗卡：{2} 登录：{3} 活跃：{4}`\n'.format(date, new_add, card, login, dau)
            pass
        return ret
    except:
        return u'服务异常'

@bot.message_handler(commands=commonds)
def send_welcome(message):
    hello = u'Hi %s:\n' % message.from_user.first_name
    if message.content_type == u'text' and message.text == u'/start' :
        bot.reply_to(message, hello + u'我是一个电报机器人, 可以快速的帮你做一些事情 你可以试试一下命令 /eos  /m2 /weather')
        pass
    elif message.content_type == u'text' and message.text == u'/weather' :
        bot.reply_to(message, hello + get_weather())
        pass
    elif message.content_type == u'text' and message.text == u'/m2':
        bot.reply_to(message, hello + get_m2(), parse_mode='Markdown')
        pass
    elif message.content_type == u'text' and message.text == u'/eos':
        bot.reply_to(message, hello + get_eos())
        pass

bot.remove_webhook()
time.sleep(0.1)
bot.set_webhook(url=config['WEBHOOK'])
app = flask.Flask(__name__)
api = Api(app)

class telegramWebhook(Resource):
    def post(self):
        if flask.request.headers.get('content-type') == 'application/json':
            try:
                json_string = flask.request.get_data().decode('utf-8')
                update = telebot.types.Update.de_json(json_string)
                bot.process_new_updates([update])
            except:
                flask.abort(403)
            return ''
        else:
            flask.abort(403)

api.add_resource(telegramWebhook, '/webhook')

if __name__ == '__main__':
    app.run(host='0.0.0.0',
        port=config['PORT'],
        ssl_context=(config['SSLPEM'], config['SSLKEY'])
	)