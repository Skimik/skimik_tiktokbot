from db_processor import Database
import time as tm
import pytz
from time import time, sleep

import telebot
from config import telegram_token
import traceback

import datetime as dt

from datetime import datetime as datetime

from driver_processor import Driver
import tikunitok
import uploader


bot = telebot.TeleBot(telegram_token, threaded=False)

class Check_machine:
    def __init__(self, bot, token=telegram_token):
        self.bot = bot

        self.keyboard = telebot.types
        self.kb_remove = self.keyboard.ReplyKeyboardRemove
        self.kb_reply = self.keyboard.ReplyKeyboardMarkup
        self.kb_inline = self.keyboard.InlineKeyboardMarkup
        self.btn_inline = self.keyboard.InlineKeyboardButton


        self.ts = 8
        self.tf = 22

        self.trs = 8
        self.trs2= 10
        self.trf = 22

        self.tpost = 15*60*60
        self.td1   = 15*60
        self.td2   = 15*60+2*60*60
        self.td3   = 15*60+7*60*60
        self.td4   = 15*60+9*60*60

        self.tt  = 2*60

        #self.tpost = 15
        #self.td1 = 1*60
        #self.td2 = 2*60
        #self.td3 = 3*60
        #self.td4 = 4*60

        #self.tt  = 2*60

        pass

    def queue_checker(self):
    
        queue_list = Database('queue_list').select_db('*','where status <> 0')

        if queue_list['available'] !=0:
            queue = queue_list['result']
            for i in range(len(queue)):
                if queue[i]['status'] == 1:

                    now = datetime.now()
                    period = dt.timedelta(days = queue[i]['period_da'],hours = queue[i]['period_ho'],minutes = queue[i]['period_mi'],seconds = 0)
                    last_ex = queue[i]['last_execute']
                    print(now)
                    print(last_ex)
                    print(period)
                    time_trigger = ((now - last_ex) - period).total_seconds()
                    print(time_trigger)
                    if time_trigger >= 5:
                        Database('queue_list').update_db('last_execute',f'"{now}"', 'where id = {}'.format(queue[i]['id']))
                        
                        x = getattr(self, queue[i]['method'])
                        x(queue[i]['id'])
                elif queue[i]['status'] == 2:
                    now = datetime.utcnow()
                    period = dt.timedelta(days = queue[i]['period_da'],hours = queue[i]['period_ho'],minutes = queue[i]['period_mi'],seconds = 0)
                    last_ex = queue[i]['last_execute']
                    print(last_ex)
                    time_trigger = ((now - last_ex) - period).total_seconds()

                    if time_trigger >= 60:
                        Database('queue_list').update_db('last_execute','"{}"'.format(queue[i]['first_execute'] + dt.timedelta(days = queue[i]['period_da'], hours = queue[i]['period_ho'],minutes = queue[i]['period_mi'],seconds = 0)), 'where id = {}'.format(queue[i]['id']))
                        Database('queue_list').update_db('status', '1', 'where id = {}'.format(queue[i]['id']))

                        x = getattr(self, queue[i]['method'])
                        x(queue[i]['id'])
                elif queue[i]['status'] == 3:
                    now = datetime.utcnow()
                    period = dt.timedelta(days = queue[i]['period_da'],hours = queue[i]['period_ho'],minutes = queue[i]['period_mi'],seconds = 0)
                    last_ex = queue[i]['last_execute']
                    print(last_ex)
                    time_trigger = ((now - last_ex) - period).total_seconds()

                    if time_trigger >= 60:
                        Database('queue_list').update_db('last_execute','"{}"'.format(queue[i]['first_execute'] + dt.timedelta(days = queue[i]['period_da'], hours = queue[i]['period_ho'],minutes = queue[i]['period_mi'],seconds = 0)), 'where id = {}'.format(queue[i]['id']))
                        Database('queue_list').update_db('status', '0', 'where id = {}'.format(queue[i]['id']))

                        x = getattr(self, queue[i]['method'])
                        x(queue[i]['id'])
    
        pass





    #def check_db(self):
    #    check_pool = Database('check_db').select_db('*','where status = 1 order by telegram_id')
    #    check_pool_res = check_pool['result']
    
    #    time_start = time()
    #    if check_pool['available'] >=1:
    #        i=0
    #        overload = False
 
    #        while i <= check_pool['available']-2:
    #            checkable_user = check_pool_res[i]['telegram_id']
    #            check_flag = True
    #            print('-   -   -',time())
    #            while i <= check_pool['available']-2 and checkable_user == check_pool_res[i+1]['telegram_id']:
    #                print(check_pool_res[i]['key_id'])
    #                print('i = ',i)
    #                checkable_user = check_pool_res[i]['telegram_id']
    #                try:
    #                    quest = self.bot.get_chat_member(check_pool_res[i]['group_id'], check_pool_res[i]['telegram_id'])
    #                    print(quest.status)
    #                    if quest.status == 'member':
    #                        if (datetime.now() - check_pool_res[i]['time_subscribe']).total_seconds() >= 3600: #86400
    #                            Database('check_db').update_db('status','2','where key_id = {}'.format(check_pool_res[i]['key_id']))
    #                            Database('user_db').update_db('exp_balance',    'exp_balance-{}'.format(check_pool_res[i]['bonus']),    'where telegram_id = {}'.format(check_pool_res[i]['telegram_id']))
    #                            Database('user_db').update_db('balance',        'balance+{}'.format(check_pool_res[i]['bonus']),        'where telegram_id = {}'.format(check_pool_res[i]['telegram_id']))
    #                    else:
    #                        check_flag = False
    #                        Database('check_db').update_db('status','0','where key_id = {}'.format(check_pool_res[i]['key_id']))
    #                except Exception as ex:
    #                    print('a    ',ex)
    #                    if 'user not found' in str(ex):
    #                        chekc_flag = False
    #                        Database('check_db').update_db('status','0','where key_id = {}'.format(check_pool_res[i]['key_id']))
    #                    elif 'bot was kicked' in str(ex):
    #                        pass
    #                        #self.bot.send_message(chat_id = 192105252, text = 'бота с села пёзднули\n{}'.format(group['result'][0]['group_link']))
    #                        #Database('job_db').update_db('admin_status','2','where group_key_id = {}'.format((group['result'][0]['group_key_id'])))
    #                        #self.bot.answer_callback_query(callback_query_id=callback_id, text='Ошибка задания. Отчет об ошибке отправлен разработчику')
    #                    elif 'bot is not a member' in str(ex):
    #                        pass
    #                        #self.bot.send_message(chat_id = 192105252, text = 'проверь целостность баз данных\n{}\nid {}'.format(group['result'][0]['group_link'],group['result'][0]['group_key_id']))
    #                        #self.bot.answer_callback_query(callback_query_id=callback_id, text='Ошибка задания. Отчет об ошибке отправлен разработчику')
    #                if check_pool['available'] < 100:
    #                    sleep(1)
    #                elif check_pool['available'] < 500:
    #                    sleep(0.5)
    #                else:
    #                    sleep(0.3)
    #                    overload = True
    #                i +=1
    #            #if check_flag == False:
    #            #    self.bot.send_message(check_pool_res[i-1]['telegram_id'], text = 'Кажется, ты отписался от одного из каналов раньше времени! Проверь раздел заданий и подпишись снова, чтобы получить вознаграждение!')
    #        else:
    #            check_flag = True
    #            print(check_pool_res[i]['key_id'])
    #            print('i = ',i)

    #            checkable_user = check_pool_res[i]['telegram_id']
    #            try:
                
    #                quest = self.bot.get_chat_member(check_pool_res[i]['group_id'], check_pool_res[i]['telegram_id'])
    #                print(quest.status)
    #                if quest.status == 'member':
    #                    if (datetime.now() - check_pool_res[i]['time_subscribe']).total_seconds() >= 3600:
    #                        Database('check_db').update_db('status','2','where key_id = {}'.format(check_pool_res[i]['key_id']))
    #                        Database('user_db').update_db('exp_balance',    'exp_balance-{}'.format(check_pool_res[i]['bonus']),    'where telegram_id = {}'.format(check_pool_res[i]['telegram_id']))
    #                        Database('user_db').update_db('balance',        'balance+{}'.format(check_pool_res[i]['bonus']),        'where telegram_id = {}'.format(check_pool_res[i]['telegram_id']))
    #                else:
    #                    check_flag = False
    #                    Database('check_db').update_db('status','0','where key_id = {}'.format(check_pool_res[i]['key_id']))
    #            except Exception as ex:
    #                print('b    ',ex)
    #                if 'user not found' in str(ex):
    #                    chekc_flag = False
    #                    Database('check_db').update_db('status','0','where key_id = {}'.format(check_pool_res[i]['key_id']))
    #                elif 'bot was kicked' in str(ex):
    #                    pass
    #                    #self.bot.send_message(chat_id = 192105252, text = 'бота с села пёзднули\n{}'.format(group['result'][0]['group_link']))
    #                    #Database('job_db').update_db('admin_status','2','where group_key_id = {}'.format((group['result'][0]['group_key_id'])))
    #                    #self.bot.answer_callback_query(callback_query_id=callback_id, text='Ошибка задания. Отчет об ошибке отправлен разработчику')
    #                elif 'bot is not a member' in str(ex):
    #                    pass
    #                    #self.bot.send_message(chat_id = 192105252, text = 'проверь целостность баз данных\n{}\nid {}'.format(group['result'][0]['group_link'],group['result'][0]['group_key_id']))
    #                    #self.bot.answer_callback_query(callback_query_id=callback_id, text='Ошибка задания. Отчет об ошибке отправлен разработчику')
    #            if check_pool['available'] < 100:
    #                sleep(1)
    #            elif check_pool['available'] < 500:
    #                sleep(0.5)
    #            else:
    #                sleep(0.3)
    #                overload = True
    #            print('last')
    #            if check_flag == False:
    #                self.bot.send_message(check_pool_res[i-1]['telegram_id'], text = 'Кажется, ты отписался от одного из каналов раньше времени! Проверь раздел заданий и подпишись снова, чтобы получить вознаграждение!')
            
        
    #        if overload == True:
    #            self.bot.send_message(chat_id = 192105252, text = 'бот близок к перегрузу')
    #    print(time())
    #    time_finish = time()-time_start
    #    return time_finish
    

    def test_quest(self,id):
        self.bot.send_message(chat_id = 192105252, text = datetime.now())

    

    def clipmaker(self, id):

        movie_queue = Database('movie').select_db('*','where iter > iter_complete')
        print(movie_queue)
        if movie_queue['available'] != 0:
            for i in range(movie_queue['available']):
                movie_to_uni = movie_queue['result'][i]['name']
                
                movie_to_uni_params = movie_queue['result'][i]['params']
                for j in range(movie_queue['result'][i]['iter'] - movie_queue['result'][i]['iter_complete']):
                    movie_to_uni_iter = movie_queue['result'][i]['iter_complete'] + j + 1

                    print(movie_to_uni_params)

                    tikunitok.parametrick_clip(name = movie_to_uni, profile = movie_to_uni_iter, params = str(movie_to_uni_params))
                    Database('movie').update_db('iter_complete', 'iter_complete+1', f'where name = "{movie_to_uni}"')





        pass




if __name__ == '__main__':
    while True:
        try:
            time_start = time()

            Check_machine(bot).queue_checker()

            time_delay = time() - time_start
            if time_delay < 10:
                print(time_delay)
                sleep(11.7 - time_delay)
            else:
                bot.send_message(chat_id = 192105252, text = 'бот близок к перегрузу')
        except Exception as ex:
            bot.send_message(chat_id = 192105252, text = 'опа, нахуй\n{}'.format(str(traceback.format_exc())))
            bot.send_message(chat_id = 192105252, text = 'тут то как что то могло сломаться, ебать, а?\n{}'.format(ex))
            sleep(14400)

        #try:
        #    resume_count = check_pool = Database('check_db').select_db('*','where status = 1')['available']
        
        #    if resume_count == 0:
        #        check_db()
        #        time_sleep = 14400
        #    else:
        #        time_sleep = 14400 - check_db()
        #    sleep(time_sleep)
        #except Exception as ex:

        #    bot.send_message(chat_id = 192105252, text = 'опа, нахуй\n{}'.format(str(traceback.format_exc())))
        #    bot.send_message(chat_id = 192105252, text = 'тут то как что то могло сломаться, ебать, а?\n{}'.format(ex))
        #    sleep(14400)
        #sleep(5)
            