import traceback
import telebot              #весь api tlgrm bot
import os.path
import requests             #зачем оно здесь, я не знаю, так было в гайде
import pymysql              #на всякий случай
from db_processor import Database         #самописный модуль
import threading            #многопоточность
import time                 #работа со временем
import json
import dumper
from fsm import Fsm
from datetime import datetime
from datetime import timedelta
from config import telegram_token
from pprint import pprint, pformat
import tikunitok
import uploader


ddos_timer = 1
pass_timer = 300

print('allah')
print(telegram_token)
bot = telebot.TeleBot(telegram_token, threaded=False)




def check_bot(message):
        if message.json['from']['is_bot'] == True:
            bot.message = bot.edit_message_text
            work = True
        elif message.json['from']['is_bot'] == False:
            bot.message = bot.send_message
            work = True
        else:
            bot.send_message(chat_id = 192105252, text = 'чувак, пиздец, вот запрос\n{}\nя вообще бля не ебу что делать спасай нахуй'.format(message))
            work = False
        return work


#стоп-спам
def stop_ddos(message, ddos_timer=ddos_timer):
    #print('------------check DDoS---------------')
    #print(message.json['from']['is_bot'])
    #if message.json['from']['is_bot'] == False:
    #    Database(table_name = 'user_db').update_db('last_mes_user_id',
    #                                               '{}'.format(message.message_id),
    #                                               'where telegram_id = {}'.format(message.chat.id))
    #    print('/////////////////////////////////////////////////')
    #if (datetime.now() - Database(table_name = 'user_db').select_db('reg_time','where telegram_id = {}'.format(message.chat.id))['result'][0]['reg_time']).total_seconds() >= 10:
    #    if (datetime.now() - Database(table_name = 'user_db').select_db('last_mes_time','where telegram_id = {}'.format(message.chat.id))['result'][0]['last_mes_time']).total_seconds() <= ddos_timer:
    #        print('------------DDoS---------------')
    #        Database(table_name = 'user_db').update_db('last_mes_time',
    #                                                   '"{}"'.format(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")),
    #                                                   'where telegram_id = {}'.format(message.chat.id))
    #        work = False
    #    else: 
    #        print('------------no DDoS---------------')
    #        work = True
    #else: 
    #    print('------------New User---------------')
    #    work = True
    return True

#проверка пользователя в базе данных
def user_checker(message):
    print('------------1==============')
    if Database(table_name = 'user_db').select_db('telegram_id','where telegram_id = {}'.format(message.chat.id))['available'] == 0:
        print('------------2==============')
        Fsm().register(message)
        keyboard_test = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)


        


@bot.message_handler(content_types=['video'])
def handle_docs_audio(message):
    print('2')
    print(message)

    Fsm().m_setting(message)

#@bot.message_handler(func=lambda message: message.document.mime_type == "video/mp4") #content_types=['document', 'gif'])
#def handle_docs_audio(message):
#    print('3')
#    print(message)

#    Fsm().m_setting(message)
 
@bot.message_handler(content_types=['animation'])
def handle_docs_audio(message):
    print('2')
    print(message)

    Fsm().m_setting(message, type = 'animation')
    

#обработка сообщения
@bot.message_handler()
def message_handler(message):
    print(message)
    handler(message = message)

#обработка инлайн кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    print(call)
    handler(message = call.message, callback_id = call.id, callback_data = call.data)

#запуск автоматов
def handler(message, callback_id = None, callback_data = None):
    print(message)
    print(callback_id)
    print(callback_data)
    user_checker(message)
    if stop_ddos(message):
        if True and ((message.chat.id == 192105252) or (message.chat.id == 518504829)):
            Fsm().executor(message, callback_id, callback_data)
        else:
            bot.send_message(chat_id = message.chat.id, text = 'бот тестируется разработчиком и не реагирует на команды')


print('akbar')
while True:
    try:
        bot.polling(none_stop= True, interval = 0.2)
    except Exception as ex:
        bot.send_message(chat_id = 192105252, text = 'чувак, пиздец, я поломался чуточкаб спасай нахуй\n{}'.format(str(traceback.format_exc())))
        bot.send_message(chat_id = 192105252, text = 'чувак, пиздец, я поломался чуточкаб спасай нахуй\n{}'.format(ex))
#        table_list = ['user_db','balance','history']
#        for i in range(len(table_list)):
#                    res = dumper.dump_db(table_list[i])
#                    if res != None:
#                        doc = open('{}'.format(res), 'rb')
#                        bot.send_document(192105252, doc)
#print('voistinu akbar')
