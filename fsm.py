import telebot
import time
import requests
import json
import dumper
from decimal import Decimal
from datetime import datetime, timedelta
from db_processor import Database
from pprint import pprint
from config import telegram_token

from random import randint

from driver_processor import Driver
import tikunitok
import uploader


class Fsm():
    def __init__(self, token=telegram_token):
        self.bot = telebot.TeleBot(token)
        self.keyboard = telebot.types
        self.kb_remove = self.keyboard.ReplyKeyboardRemove
        self.kb_reply = self.keyboard.ReplyKeyboardMarkup
        self.kb_inline = self.keyboard.InlineKeyboardMarkup
        self.btn_inline = self.keyboard.InlineKeyboardButton

        self.commands = {
                        'домой':'home',
                        '/start':'home',
                        'добавить аккаунт':'account',
                        'skimik_dump':'dumping',
                        'skimik_test':'test',
                        'info':'manual',
                        'выгрузка':'u_change',
                        'добавить видео':'video_stat'
                        }


#исполнитель запросов
    def executor(self, message, callback_id=None, callback_data=None):
        user_db = Database(table_name = 'user_db').select_db('*','where telegram_id = {}'.format(message.chat.id))

        if message.text.lower() in self.commands:
            print('---------------------------------commands-------------------------------------')
            x = getattr(self, self.commands[message.text.lower()])
            x(message, callback_id, callback_data)

        
            
        elif callback_data != None:
            print('---------------------------------inlinebtn------------------------------------')
            data = callback_data.split(', ')
            print(data)
            fsm_code = int(data[0])
            fsm_wait = int(data[1])
            fsm_param = str(data[2])
            call_point = Database('fsm').select_db('*','where track = {}'.format(fsm_code))
            db_point = Database('fsm').select_db('*','where track = {}'.format(user_db['result'][0]['fsm_code']))
            if  (call_point['available'] != 0 and db_point['available'] != 0):
                if (call_point['result'][0]['point_a'] == db_point['result'][0]['point_b'] or 
                    call_point['result'][0]['point_a'] == "all"):
                    x = getattr(self, call_point['result'][0]['point_b'])
                    x(message, callback_id, callback_data)
                else: print('--------- ошибка последовательности автоматов. автомат проигнорирован ---------')
            else: print('--------- ошибка наличия автоматов. автомат проигнорирован ---------')
        elif user_db['result'][0]['fsm_wait'] != 0:
            print('---------------------------------2-------------------------------------')
            print(Database('fsm').select_db('*','where track = {}'.format(int(user_db['result'][0]['fsm_wait']))))
            x = getattr(self, Database('fsm').select_db('*','where track = {}'.format(user_db['result'][0]['fsm_wait']))['result'][0]['point_b'])
            x(message, callback_id, callback_data)

        elif len(message.text.split(' ')) ==3:
            print('------------------------------link1--------------------------')
            link = message.text.split(' ')
            if link[1].isdigit() and link[2].isdigit():
                print('------------------------------link2--------------------------')
                text_link = ''
                if link[0][:8] == 'https://':
                    print('------------------------------link3--------------------------')
                    text_link = link[0][8:]
                if link[0][:7] == 'http://':
                    print('------------------------------link3--------------------------')
                    text_link = link[0][7:]
                    
                else: text_link = link[0]
                if text_link != '':
                    self.buy_1(message, callback_id, callback_data, text_link)

        else: 
            self.default(message, callback_id, callback_data)
            print('--------- ошибка обработки запроса. автомат не выполнен ---------')
    

    def db_user_info(self, id = None):
        user_info = Database(table_name = 'user_db').select_db('*','where telegram_id = {}'.format(id))
        if user_info['available'] == 0:
            Database(table_name = 'user_db').insert_db(values = ['{}'.format(message.chat.id),		#telegram_id=
                                                                '"{}"'.format(message.chat.username),	#username
                                                               
                                                                '0',		#fsm_code=
                                                                '0',		#fsm_wait=
                                                                '"None"'	#fsm_param=
                                                              
                                                                ])
            user_info = Database(table_name = 'user_db').select_db('*','where telegram_id = {}'.format(id))
        return user_info

#запись данных исполненного автомата в базу данных пользователей	
    def fsm_db(self, message, fsm_code=None, fsm_wait=None, fsm_param=None, callback_data=None):
        if callback_data != None:
            data = callback_data.split(', ')
            fsm_code = int(data[0])
            fsm_wait = int(data[1])
            fsm_param = str(data[2])
        Database(table_name = 'user_db').update_db('fsm_code',
                                                   '{}'.format(fsm_code),
                                                   'where telegram_id = {}'.format(message.chat.id))
        Database(table_name = 'user_db').update_db('fsm_wait',
                                                   '{}'.format(fsm_wait),
                                                   'where telegram_id = {}'.format(message.chat.id))
        if fsm_param != None:
            Database(table_name = 'user_db').update_db('fsm_param',
                                                       '"{}"'.format(fsm_param),
                                                       'where telegram_id = {}'.format(message.chat.id))

#модифицированный метод отправки сообщения
    def send_message(self, message, text, keyboard_reply = None, callback_id=None, callback_data=None):
        msg = self.bot.send_message(chat_id=message.chat.id, 
                                    text= text,
                                    reply_markup = keyboard_reply)
        #Database(table_name = 'user_db').update_db('last_mes_bot_id',
        #                                           '"{}"'.format(msg.message_id),
        #                                           'where telegram_id = {}'.format(message.chat.id))
        return msg

    #я не помню, что это
    def update_mes(self, message, update_types, update_param='None'):
        Database('update_mes').delete_db('where telegram_id = {}'.format(message.chat.id))
        Database('update_mes').insert_db(values = ['{}'.format(message.chat.id),
                                                   '{}'.format(message.message_id),
                                                   '{}'.format(update_types),
                                                   '"{}"'.format(update_param),
                                                   '"{}"'.format(datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"))])

    #уже не нужно
    def test(self,  message, callback_id=None, callback_data=None):
        if message.chat.id == 192105252:
            keyboard_reply = self.kb_reply(resize_keyboard = True)
            keyboard_reply.add('домой')
            keyboard_inline = self.kb_inline()
            msg = self.edit_message_reply(message, 
                              text=datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S",),
                              keyboard_inline = keyboard_reply)
            self.update_mes(msg, update_types = 0)

    #эта штука при любой возможности стремится сбросить твоё состояние до Home
    def default(self,  message, callback_id=None, callback_data=None):
        keyboard_reply = self.kb_reply(resize_keyboard = True)
        keyboard_reply.add('Домой')
        self.send_message(message, 
                          'неактивный раздел\n ' + datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S",),
                          keyboard_reply)


    def dumping(self, message, callabck_id, callback_data):
        if message.chat.id == 192105252:
            table_list = ['user_db','balance','history']
            for i in range(len(table_list)):
                res = dumper.dump_db(table_list[i])
                if res != None:
                    doc = open('{}'.format(res), 'rb')
                    self.bot.send_document(192105252, doc)
                    
                
            print('я всё. отпевайте.')
            
#домашняя страница
    def home(self, message, callback_id=None, callback_data=None):
        
        keyboard_inline = self.kb_inline()

        keyboard_reply = self.kb_reply(resize_keyboard = True)
        keyboard_reply.add('добавить аккаунт')
        keyboard_reply.add('добавить видео')
        keyboard_reply.add('выгрузка')
        keyboard_reply.add('info')
        #keyboard_reply.add('доступные видео')
        

        self.send_message(message, 
                          'тикток-автоматизатор\nбета-версия клиента\nv0.29.2',
                          keyboard_reply)
        self.fsm_db(message, 3, 0, 'None')
            

    def register(self, message):
        if Database(table_name = 'user_db').select_db('telegram_id','where telegram_id = {}'.format(message.from_user.id))['available'] == 0:
            
            Database(table_name = 'user_db').insert_db(values = ['{}'.format(message.chat.id),		#telegram_id=
                                                                '"{}"'.format(message.chat.username),	#username
                                                               
                                                                '0',		#fsm_code=
                                                                '0',		#fsm_wait=
                                                                '"None"'	#fsm_param=
                                                              
                                                                ])
        #self.home(message)












    def account(self, message, callback_id=None, callback_data=None):
        uid = message.chat.id

        keyboard_inline = self.kb_inline()
        auth_btn = self.btn_inline(text="запрос на аутентификацию", callback_data="8, 0, None")
        
        add_btn = self.btn_inline(text="добавить аккаунт", callback_data="5, 0, None")
        keyboard_inline.add(auth_btn)
        keyboard_inline.add(add_btn)

        auth_list = Database('auth').select_db('*',f'where telegram_id = {uid} and auth_status = 1')['available']
        all_list = Database('auth').select_db('*',f'where telegram_id = {uid}')['available']
        

        text =  '➖➖➖➖➖➖➖➖➖➖\n'
        text +=  f'\nколичество активированных аккаунтов - {auth_list}\n\n всего аккаунтов - {all_list}\n\n'      
        if all_list>auth_list:
            text +='активация в процессе'
        else:
            text +='активация завершена'
        text += '➖➖➖➖➖➖➖'

        self.send_message(message, 
                          text=text,
                          keyboard_reply = keyboard_inline)

        self.fsm_db(message, 4, 0, 'None')


        pass

    def acc_add(self, message, callback_id=None, callback_data=None):
        uid = message.chat.id
        if callback_data != None:
            
            keyboard_inline = self.kb_inline()

            keyboard_reply = self.kb_reply(resize_keyboard = True)
            keyboard_reply.add('домой')
           
            text =  'введите через пробел следующие данные\n'
            text += 'username email password\n'    
            text += 'можно вводить сразу несколько аккаунтов (на 1 аккаунт 1 сообщение)\n'
            text += 'каждый раз жать кнопку добавить аккаунт НЕ НУЖНО\n'
            text += 'достаточно нажать её один раз и потом по 1 сообщению отправлять все данные\n'
            text += 'ввод данных большой группой - в разработке\n'
            text += 'для завершения ввода нажмите кнопку домой' 

            self.send_message(message, 
                              text=text, keyboard_reply = keyboard_reply)

            self.fsm_db(message, 5, 6, 'None')

        else:
            data = message.text.split(' ')
            username= data[0]
            email   = data[1]
            password= data[2]

            if (
                (Database('auth').select_db('*',f'where email = "{email}"')['available'] == 0) and 
                (Database('auth').select_db('*',f'where username = "{username}" and telegram_id = "{uid}"')['available'] == 0)
                ):

                last_id = Database('auth').select_db('id', f'where telegram_id = "{uid}"')['available']
                Database('auth').insert_db(values = [   f'{uid}',
                                                        f'{last_id+1}',
                                                        f'"{username}"',
                                                        f'"{email}"',
                                                        f'"{password}"',
                                                        '0'
                                                    ])
                text = 'аккаунт добавлен, готов продолжать'
            else:
                text = 'аккаунт с таким email или username уже имеется'


            self.send_message(message, 
                              text=text)
            self.fsm_db(message, 6, 6, 'None')


        pass

    def acc_auth(self, message, callback_id=None, callback_data=None):



        uid = message.chat.id

        #keyboard_inline = self.kb_inline()
        #auth_btn = self.btn_inline(text="аутентификация", callback_data="11, 0, None")
        #add_btn = self.btn_inline(text="добавить аккаунт", callback_data="11, 0, None")
        #keyboard_inline.add(url_button)
        #keyboard_inline.add(callback_button)

        text =  'Запрос на авторизацию отправлен. ожидайте результатов в ближайшее время\n'
        text += 'процесс аутентификации аккаунтов занимает некоторое время. каждый аккаунт аутентифицируется от 30 до 90 секунд\n'        
        text += 'в течение этого времени бот будет не активен. по окончании процесса аутентификации бот пришлёт соответствующее сообщение\n'
        text += 'ожидайте'

        self.send_message(message, 
                          text=text)

        self.admin_auth_start(self, message)

        self.fsm_db(message, 8, 0, 'None')


        #auth_list = Database('auth').select_db('*',f'where telegram_id = {uid} and auth_status = 0')
        #if auth_list['available'] !=0:
        #    for i in range(auth_list['available']):
        #        self.bot.send_message(192105252, 
        #                                text=str(auth_list['result'][i]['username'])+'\n_ '+str(auth_list['result'][i]['email'])+'\n_ '+str(auth_list['result'][i]['password'])+'\n_ '+str(auth_list['result'][i]['auth_status']))
        #        res = uploader.auth(auth_list['result'][i]['username'], auth_list['result'][i]['email'], auth_list['result'][i]['password'], auth_list['result'][i]['auth_status'])
        #        if res:
        #            text = f'acc {auth_list["result"][i]["username"]} yes'
        #            Database('auth').update_db('auth_status','1',f'where email = "{auth_list["result"][i]["email"]}"')
        #        else:
        #            text = f'acc {auth_list["result"][i]["username"]} no'
        #        self.send_message(message, text=text)
        #self.send_message(message, text='end auth')
        #self.home(message)

        pass



    def acc_auth_test(self, message, callback_id=None, callback_data=None):
        uid = message.chat.id

        #keyboard_inline = self.kb_inline()
        #auth_btn = self.btn_inline(text="аутентификация", callback_data="11, 0, None")
        #add_btn = self.btn_inline(text="добавить аккаунт", callback_data="11, 0, None")
        #keyboard_inline.add(url_button)
        #keyboard_inline.add(callback_button)

        text =  '➖➖➖➖➖➖➖➖➖➖\n'
        text += 'процесс аутентификации аккаунтов занимает некоторое время. каждый аккаунт аутентифицируется от 30 до 90 секунд. Аутентификация происходит в полуавтоматическом режиме.\n'        
        text += 'Аутентификация начнётся в ближайшее время. по окончании процесса аутентификации бот пришлёт соответствующее сообщение\n'
        text += 'ожидайте'

        self.send_message(message, 
                          text=text)

        self.fsm_db(message, 8, 0, 'None')


        auth_list = Database('auth').select_db('*',f'where telegram_id = {uid} and auth_status = 0')
        if auth_list['available'] !=0:
            #for i in range(auth_list['available']):
                i = 0
                self.bot.send_message(192105252, 
                                        text=str(auth_list['result'][i]['username'])+'\n_ '+str(auth_list['result'][i]['email'])+'\n_ '+str(auth_list['result'][i]['password'])+'\n_ '+str(auth_list['result'][i]['auth_status']))
                res = uploader.auth_test(auth_list['result'][i]['username'], auth_list['result'][i]['email'], auth_list['result'][i]['password'], auth_list['result'][i]['auth_status'])
                if res:
                    text = f'acc {auth_list["result"][i]["username"]} yes'
                    Database('auth').update_db('auth_status','1',f'where email = "{auth_list["result"][i]["email"]}"')
                else:
                    text = f'acc {auth_list["result"][i]["username"]} no'
                self.send_message(message, text=text)
        self.send_message(message, text='end auth')
        self.home(message)

        pass





    def m_setting(self, message, callback_id=None, callback_data=None, type = 'video'):

        uid = message.chat.id

        keyboard_inline = self.kb_inline()
        btn1 = self.btn_inline(text="1", callback_data="11, 0, 1")
        btn2 = self.btn_inline(text="1", callback_data="11, 0, 2")
        btn3 = self.btn_inline(text="1", callback_data="11, 0, 3")
        keyboard_inline.add(btn1)
        keyboard_inline.add(btn2)
        keyboard_inline.add(btn3)

        text =  '➖➖➖➖➖➖➖➖➖➖\n'
        text += 'уникализатор v0.79.513 эксепериментальная сборка\n\n'        
        text += 'параметры уникализации\n\n' 
        text += 'поворот 0-10\n' 
        text += 'рамка 0-10\n' 
        text += 'шум 0-10\n' 
        text += 'блюр на фоне 0-1\n' 
        text += 'контраст 0-10\n' 
        text += 'миррор 0-2\n'
        text += 'для настройки уникализатора введите через пробел все параметры в указанных диапазонах\n'
        
        if type == 'video':
            video_id = message.video.file_id
            file_id_info = self.bot.get_file(message.video.file_id)
        else:
            video_id = message.animation.file_id
            file_id_info = self.bot.get_file(message.animation.file_id)

       

        
        downloaded_file = self.bot.download_file(file_id_info.file_path)
    
        #x = datetime.strftime(datetime.now(), "%Y-%m-%d_%H_%M_%S")
        #name = f'{message.caption}'
        last_id = Database('movie').select_db('id', f'where telegram_id = "{uid}"')['available']

        name = f'm_{uid}_{last_id+1}'





        with open(name+'.mp4', 'wb') as new_file:
            new_file.write(downloaded_file)
    
        new_file.close()
        

        Database('movie').insert_db(values = [
                                            f'{uid}',
                                            f'"{name}"',
                                            '0',
                                            '0',
                                            '"None"',
                                            f'{last_id+1}'
                                            ])


        #if message.caption != None:
        #    capt = open('capt.txt','w')
        #    capt.write(message.caption)
        #    capt.close()
        #else:
        #    capt = open('capt.txt','w')
        #    capt.write('no')
        #    capt.close()

        self.send_message(message, 
                          text=text,
                          keyboard_reply = keyboard_inline)

        self.fsm_db(message, 10, 11, last_id+1)

    def m_count(self, message, callback_id=None, callback_data=None):
        uid = message.chat.id
        params = message.text.split(' ')
        if len(params) == 6:
            m_id = Database('user_db').select_db('*',f'where telegram_id = {uid}')['result'][0]['fsm_param']
            Database('movie').update_db('params',f'"{message.text}"',f'where telegram_id = {uid} and id = {m_id}')

        auth_list = Database('auth').select_db('*',f'where telegram_id = {uid} and auth_status = 1')['available']
        all_list = Database('auth').select_db('*',f'where telegram_id = {uid}')['available']
        text =  f'введите количество копий видео. количество активированных аккаунтов - {auth_list}, всего аккаунтов - {all_list}\n'
        self.send_message(message, 
                          text=text)

        self.fsm_db(message, 11, 12, m_id)

    def m_render(self, message, callback_id=None, callback_data=None):
        uid = message.chat.id
        m_id = Database('user_db').select_db('*',f'where telegram_id = {uid}')['result'][0]['fsm_param']
        count = message.text
        if int(count) !=0:
            Database('movie').update_db('iter',f'{count}',f'where telegram_id = {uid} and id = {m_id}')
        auth_list = Database('auth').select_db('*',f'where telegram_id = {uid} and auth_status = 1')['available']
        all_list = Database('auth').select_db('*',f'where telegram_id = {uid}')['available']
        text =  f'введите описания для видео. количество активированных аккаунтов - {auth_list}, всего аккаунтов - {all_list}\n'
        self.send_message(message, 
                          text=text)

        self.fsm_db(message, 12, 13, m_id)

    def m_fin(self, message, callback_id=None, callback_data=None):
        uid = message.chat.id
        #desc = message.text.split(';')
        m_id = Database('user_db').select_db('*',f'where telegram_id = {uid}')['result'][0]['fsm_param']
        if message.text.lower() != 'no':
            capt = open(f'c_{uid}_{m_id}.txt','w')
            capt.write(message.text)
            capt.close()
        else:
            capt = open(f'c_{uid}_{m_id}.txt','w')
            capt.write('no')
            capt.close()

        text =  f'фоновая обработка запущена\n'
        self.send_message(message, 
                          text=text)

        self.fsm_db(message, 13, 0, m_id)




    def u_change(self, message, callback_id=None, callback_data=None):
        uid = message.chat.id
        text =  f'доступные видео\n'
        m_list = Database('movie').select_db('*',f'where telegram_id = {uid} and iter = iter_complete and iter > 0')
        if m_list['available'] !=0:
            for i in range(m_list['available']):
                id = m_list['result'][i]['id']
                text += f'{id} '

            text += '\nвведите номер видео для загрузки'
            self.send_message(message, text)

            self.fsm_db(message, 14, 15, 0)
        else:
            text = 'видео не загружены или ещё находятся в обработке.'
            self.send_message(message, text)
            self.home(message)


    def u_upload(self, message, callback_id=None, callback_data=None):
        uid = message.chat.id
        i = 0


        m_id = Database('user_db').select_db('*',f'where telegram_id = {uid}')['result'][0]['fsm_param']

        m_id = int(message.text)

        m_dat = Database('movie').select_db('*',f'where telegram_id = {uid} and iter = iter_complete and iter > 0 and id = {m_id}')
        if m_dat['available'] != 0:

            for i in range(m_dat['result'][0]['iter']):
                name = m_dat['result'][0]['name']
                profile = i+1
                m_name = 'out\\'+f"{name}_{profile}.mp4"
                docum = open(m_name, 'rb')
                try:
                    self.bot.send_video(message.chat.id , docum)
                except:
                    self.send_message(message, text = 'файл слишком большой для телеграма, не могу загрузить')
            keyboard_inline = self.kb_inline()
            btn1 = self.btn_inline(text="go", callback_data=f"17, 0, {m_id}")
            btn2 = self.btn_inline(text="set delay", callback_data=f"18, 0, {m_id}")
            keyboard_inline.add(btn1)
            
            self.send_message(message, 
                            text='upload?',
                            keyboard_reply = keyboard_inline)
        else:
            self.send_message(message, 
                            text='видео не найдено, обратитесь к администратору')


        self.fsm_db(message, 15, 0, m_id)

    def u_fin(self, message, callback_id=None, callback_data=None):
        uid = message.chat.id

        m_id = Database('user_db').select_db('*',f'where telegram_id = {uid}')['result'][0]['fsm_param']

        

        m_dat = Database('movie').select_db('*',f'where telegram_id = {uid} and iter = iter_complete and iter > 0 and id = {m_id}')

        
        name = m_dat['result'][0]['name']
        profile = 1
         
        m_name = 'out\\'+f"{name}_{profile}.mp4"



        auth_list = Database('auth').select_db('*',f'where telegram_id = {uid} and auth_status = 1')
        self.send_message(message, text = f'начинаю загрузку в {auth_list["available"]} итерации')
        print(auth_list)
        trig = 0
        capt = open(f'c_{uid}_{m_id}.txt','r')
        caption = capt.read()
        capt.close()
        if caption !='no':
            trig = 1


        if auth_list['available'] == 1:
            username = auth_list['result'][0]['username']

            if trig ==1:
                desc = caption.split(';')
                desc1 = desc[randint(0,len(desc)-1)]
                uploader.up(f'{username}', m_name, desc1)
            else:
                uploader.up(f'{username}', m_name)
            self.send_message(message, text = f'итерация {1} готова')
        elif auth_list['available'] > 1:
            i = 0
            while i<=auth_list['available']-1:
                m_name = 'out\\'+f"{name}_{profile}.mp4"
                username = auth_list['result'][i]['username']
                if trig ==1:
                    desc = caption.split(';')
                    desc1 = desc[randint(0,len(desc)-1)]
                    uploader.up(f'{username}', m_name, desc1)
                else:
                    uploader.up(f'{username}', m_name)
                self.send_message(message, text = f'итерация {i+1} готова')
                i+=1
                
                profile = profile % m_dat['result'][0]['iter']
                profile += 1
                
        self.home(message)




    def u_delay(self, message, callback_id=None, callback_data=None):







        pass

    def distribution_0(self, message, callback_id = None, callback_data = None):
        self.send_message(message, 
                          'напиши текст рассылки в следующем виде. id <id>;<сообщение> \nпример\n\nid 192105252;слава бот сломался\n\nобязателен знак ;\n\nдля отправки сообщения ВСЕМ формат такой\n\nALL;<текст сообщения>')
        self.fsm_db(message, 19, 20, 'None')


    def distribution_1(self, message, callback_id = None, callback_data = None):

        queue_list = Database('queue_list').select_db('id')
        queue = open('md_{}.txt'.format(queue_list['available']+1), 'w')
        queue.write(message.text)
        queue.close()


        text ='введи дату первого выполнения рассылки и периодичность выполнения в формате ГГГГ-ММ-ДД чч:мм:сс ; Д ч м\nГ-год \nМ-месяц \nД-день \nч-час \nм-минута \nс-сеунда'
        self.bot.send_message(message.chat.id, text)
        self.fsm_db(message, 20, 21, 'None')


        pass

    def distribution_complete(self, message, callback_id = None, callback_data = None):
        try:
            if ';' in message.text:
                data = message.text.split(';')
                g_datetime = str(data[0])
                p = data[1].strip().split(' ')
        
                Database('queue_list').insert_db(column =[  'status',
                                                            'period_mi',
                                                            'period_ho',
                                                            'period_da',
                                                            'method',
                                                            'first_execute',
                                                            'last_execute'],
                                                values =['1',
                                                        '{}'.format(p[2]),
                                                        '{}'.format(p[1]),
                                                        '{}'.format(p[0]),
                                                        '"message_distribution"',
                                                        '"{}"'.format(g_datetime),
                                                        '"{}"'.format(g_datetime)
                                                        ])
            else:
                data = message.text
                g_datetime = str(data)
            
        
                Database('queue_list').insert_db(column =[  'status',
                                                            'period_mi',
                                                            'period_ho',
                                                            'period_da',
                                                            'method',
                                                            'first_execute',
                                                            'last_execute'],
                                                values =['3',
                                                        '0',
                                                        '0',
                                                        '0',
                                                        '"message_distribution"',
                                                        '"{}"'.format(g_datetime),
                                                        '"{}"'.format(g_datetime)
                                                        ])
            self.bot.send_message(message.chat.id, 'задание сохранено')
        except:
            self.bot.send_message(message.chat.id, 'задание не сохранено. ошибка данных')
        self.home(message)





    def movie(self, message, callback_id=None, callback_data=None):

        uid = message.chat.id

        keyboard_inline = self.kb_inline()
        btn1 = self.btn_inline(text="1", callback_data="11, 0, 1")
        btn2 = self.btn_inline(text="1", callback_data="11, 0, 2")
        btn3 = self.btn_inline(text="1", callback_data="11, 0, 3")
        keyboard_inline.add(btn1)
        keyboard_inline.add(btn2)
        keyboard_inline.add(btn3)

        text =  '➖➖➖➖➖➖➖➖➖➖\n'
        text += 'уникализатор v0.79.513 эксепериментальная сборка\n\n'        
        text += 'параметры уникализации\n\n' 
        text += 'поворот 0-10\n' 
        text += 'рамка 0-10\n' 
        text += 'шум 0-10\n' 
        text += 'блюр на фоне 0-1\n' 
        text += 'контраст 0-10\n' 
        text += 'миррор 0-2\n'
        text += 'для настройки уникализатора введите через пробел все параметры в указанных диапазонах\n'
        



        video_id = message.video.file_id

        file_id_info = self.bot.get_file(message.video.file_id)
        downloaded_file = self.bot.download_file(file_id_info.file_path)
    
        x = datetime.strftime(datetime.now(), "%Y-%m-%d_%H_%M_%S")
        #name = f'{message.caption}'
        name = f'{x}'
        with open(name+'.mp4', 'wb') as new_file:
            new_file.write(downloaded_file)
    
        new_file.close()
        if message.caption != None:
            capt = open('capt.txt','w')
            capt.write(message.caption)
            capt.close()
        else:
            capt = open('capt.txt','w')
            capt.write('no')
            capt.close()

        self.send_message(message, 
                          text=text,
                          keyboard_reply = keyboard_inline)

        self.fsm_db(message, 10, 11, name)






        pass


    def movie_2(self, message, callback_id=None, callback_data=None):
        uid = message.chat.id


        text_preset = 'пресеты пока не работают. используйте ручную настройку'
        if callback_data != None:
            data = callback_data.split(', ')
            fsm_code = int(data[0])
            fsm_wait = int(data[1])
            fsm_param = int(data[2])
            print(fsm_param)

        name = Database('user_db').select_db('*',f'where telegram_id = {uid}')['result'][0]['fsm_param']

        auth_list = Database('auth').select_db('*',f'where telegram_id = {uid} and auth_status = 1')

        self.send_message(message, text = 'имя файла '+name)
        self.send_message(message, text = f'начинаю обработку в {auth_list["available"]} итерации')
        print(range(auth_list['available']))
        if auth_list['available'] == 1:
            if callback_data != None:
                self.send_message(message, text)
                #print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                ##print(fsm_param)
                #username = auth_list['result'][0]['username']
                #tikunitok.clips(name, username, fsm_param)
                #self.send_message(message, text = f'итерация {1} готова')
                #docum = open(name+f'_{username}_1.mp4', 'rb')
                #self.bot.send_video(message.chat.id , docum)
                #docum.close()
            else:
                    username = auth_list['result'][0]['username']
                    print('ffassdfaf')
                    params = message.text.split(' ')
                    print('fqaadfafff')
                    tikunitok.parametrick_clip(name, username, params)
                    print('fqsdgwergff')

                    self.send_message(message, text = f'итерация {1} готова')
                    docum = open(name+f'_{username}.mp4', 'rb')
                    try:
                        self.bot.send_video(message.chat.id , docum)
                    except:
                        self.send_message(message, text = text_preset)

                    docum.close()
                    
        elif auth_list['available'] > 1:
            i = 0
            while i<=auth_list['available']-1:
                if callback_data != None:
                    self.send_message(message, text = text_preset)
                    #print(i)
                    #print(range(auth_list['available']-1))
                    #print('aaaaabbbbbbbbbaa')
                    ##print(fsm_param)
                    #username = auth_list['result'][i]['username']
                    #tikunitok.clips(name, username, fsm_param)
                    #self.send_message(message, text = f'итерация {i+1} готова')
                    #docum = open(name+f'_{username}.mp4', 'rb')
                    try:
                        self.bot.send_video(message.chat.id , docum)
                    except:
                        self.send_message(message, text = 'файл слишком большой для телеграма, не могу загрузить')

                    docum.close()
                    i+=1
                else:
                    username = auth_list['result'][i]['username']
                    print('ffassdfaf')
                    params = message.text.split(' ')
                    print('fqaadfafff')
                    tikunitok.parametrick_clip(name, username, params)
                    print('fqsdgwergff')

                    self.send_message(message, text = f'итерация {i+1} готова')
                    docum = open(name+f'_{username}.mp4', 'rb')
                    try:
                        self.bot.send_video(message.chat.id , docum)
                    except:
                        self.send_message(message, text = 'файл слишком большой для телеграма, не могу загрузить')

                    docum.close()
                    i+=1

        keyboard_inline = self.kb_inline()
        btn1 = self.btn_inline(text="go", callback_data="13, 0, 0")
            
        keyboard_inline.add(btn1)
            
        self.send_message(message, 
                        text='upload?',
                        keyboard_reply = keyboard_inline)

        self.fsm_db(message, 11, 0, name)


    def movie_3(self, message, callback_id=None, callback_data=None):
        uid = message.chat.id
        name = Database('user_db').select_db('*',f'where telegram_id = {uid}')['result'][0]['fsm_param']
        auth_list = Database('auth').select_db('*',f'where telegram_id = {uid} and auth_status = 1')
        self.send_message(message, text = f'начинаю загрузку в {auth_list["available"]} итерации')
        print(auth_list)
        trig = 0
        capt = open('capt.txt','r')
        caption = capt.read()
        capt.close()
        if caption !='no':
            trig = 1


        if auth_list['available'] == 1:
            username = auth_list['result'][0]['username']

            if trig ==1:
                desc = caption.split(';')
                desc1 = desc[randint(0,len(desc)-1)]
                uploader.up(f'{username}', name+f'_{username}.mp4', desc1)
            else:
                uploader.up(f'{username}', name+f'_{username}.mp4')
            self.send_message(message, text = f'итерация {1} готова')
        elif auth_list['available'] > 1:
            i = 0
            while i<=auth_list['available']-1:

                username = auth_list['result'][i]['username']
                if trig ==1:
                    desc = caption.split(';')
                    desc1 = desc[randint(0,len(desc)-1)]
                    uploader.up(f'{username}', name+f'_{username}.mp4', desc1)
                else:
                    uploader.up(f'{username}', name+f'_{username}.mp4')
                self.send_message(message, text = f'итерация {i+1} готова')
                i+=1
                
        self.home(message)



    def admin_auth_start(self, message, callback_id=None, callback_data=None):

        keyboard_inline = self.kb_inline()
        auth_btn = self.btn_inline(text="начать", callback_data="29, 0, None")
        
        
        keyboard_inline.add(auth_btn)
        

        text =  '➖➖➖➖➖➖➖➖➖➖\n'
        text += 'ну чё, погнали?\n'        
        text += '➖➖➖➖➖➖➖'

        self.bot.send_message(192105252, 
                          text=text,
                          reply_markup = keyboard_inline)
        
        #self.fsm_db(message, 25, 0, 'None')

        pass


    def admin_auth(self, message, callback_id=None, callback_data=None):

        keyboard_inline = self.kb_inline()
        auth_btn = self.btn_inline(text="next", callback_data="28, 0, None")
        
        
        keyboard_inline.add(auth_btn)


        
        auth_list = Database('auth').select_db('*','where auth_status = 0')
        if auth_list['available'] !=0:
            #for i in range(auth_list['available']):
                i = 0
                self.bot.send_message(192105252, 
                                        text=str(auth_list['result'][i]['username'])+'\n_ '+str(auth_list['result'][i]['email'])+'\n_ '+str(auth_list['result'][i]['password'])+'\n_ '+str(auth_list['result'][i]['auth_status']))
                res = uploader.auth(auth_list['result'][i]['username'], auth_list['result'][i]['email'], auth_list['result'][i]['password'], auth_list['result'][i]['auth_status'])
                if res:
                    text = f'acc {auth_list["result"][i]["username"]} yes; last {auth_list["available"]}'
                    Database('auth').update_db('auth_status','1',f'where email = "{auth_list["result"][i]["email"]}"')
                else:
                    text = f'acc {auth_list["result"][i]["username"]} no; last {auth_list["available"]}'
                self.send_message(message, text=text)
                self.send_message(message, text='auth', keyboard_reply = keyboard_inline)
        else:
            self.home(message)

        pass











    def manual(self, message, callback_id, callback_data):

        text = 'для загрузки видео просто отправьте видео в этот чат\n\n'
        text +='для добавления описания к видео напишите 2 и более вариантов описания в комментарии к загружаемому видео в следующем формате\n\n'
        text +='первое описание ; второе описание ; третье описание\n\n'
        text +='бот будет добавлять случайное описание из этого списка каждому видео'

        
        self.send_message(message, text)


    def video_stat(self, message, callback_id, callback_data):
        uid = message.chat.id
        m_c = Database('movie').select_db('*',f'where telegram_id = {uid}')
        text = 'статистика видео\n\n'
        for i in range(m_c['available']):
            id = m_c['result'][i]['id']
            name = m_c['result'][i]['name']
            count = m_c['result'][i]['iter']
            complete = m_c['result'][i]['iter_complete']
            if int(count) - int(complete) > 0:
                text+=f'id = {id}\n'
                text+=f'_    name = {name}\n'
                text+=f'_    count = {count}\n'
                text+=f'_    complite = {complete}\n'
            else:
                text+=f'id = {id} !!!SUCCES!!!\n'


        text+='\nдля загрузки видео просто отправьте его боту'
        self.send_message(message, text)