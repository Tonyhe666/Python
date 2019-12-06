# !/usr/bin/python
# _*_ coding:utf-8 _*_
import telebot
from telebot import types
import requests
from telebot import apihelper

apihelper.proxy = {'http':'http://127.0.0.1:1087', 'https':'http://127.0.0.1:1087'}

bot = telebot.TeleBot('867011198:AAF0eUYF6FdUM7ev2fa9FfE55rAmx_z_NjE')
commonds = ['start', 'm2', 'eos', 'weather', 'chatid']

def test(commands=commonds):
    return commands

@bot.message_handler(commands=commonds)
def handle_commands(message):
    hello = u'Hi %s:\n' % message.from_user.first_name
    if message.content_type == u'text' and message.text == u'/start' :
        bot.reply_to(message, hello + u'我是一个电报机器人, 可以快速的帮你做一些事情 你可以试试一下命令 /eos  /m2 /weather')
        pass
    elif message.content_type == u'text' and message.text == u'/weather' :
        bot.reply_to(message, hello + message.chat.username + str(message.chat.id))
        pass
    elif message.content_type == u'text' and message.text == u'/m2':
        bot.reply_to(message, hello + message.chat.username + str(message.chat.id), parse_mode='Markdown')
        pass
    elif message.content_type == u'text' and message.text == u'/eos':
        bot.reply_to(message, hello + message.chat.username + str(message.chat.id))
        pass
    elif message.content_type == u'text' and message.text == u'/chatid':
        #bot.reply_to(message, hello + message.chat.username + str(message.chat.id))
        bot.send_message(chat_id=538661911, text=message.from_user.id)
        pass


bot.polling(none_stop=False, interval=0, timeout=20)