import xlsxwriter
from db_processor import Database as db
from time import time, sleep
from datetime import datetime

table_list = ['user_db','balance','history']

def dump_db(table_name):

    #------------------------------------------Создание объекта - файла-------------------------------------------------------------------
    name = '{}_{}.xlsx'.format(table_name,datetime.strftime(datetime.now(), "%Y-%m-%d_%H_%M_%S"))
    workbook = xlsxwriter.Workbook(name)
    #------------------------------------------------Создание нового листа в файле Excel-----------------------------------------------------------
    worksheet = workbook.add_worksheet()
    parsing_db = db('{}'.format(table_name)).select_db('*')
    flag = False
    if parsing_db['available'] != 0:
        alph = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        height = len(parsing_db['result'])
        width = len(parsing_db['result'][0])
        key = list(parsing_db['result'][0])

        for i in range(height):
            for j in range(width):

                worksheet.write_string(i+1,j+1,str(parsing_db['result'][i]['{}'.format(key[j] ) ]) )

        workbook.close()
        flag = True
        print('дамп таблицы {} вроде как успешно сохранён под eminem {}_{}.xslx'.format(table_name,table_name,datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S")))
    else:
        print('таблица {} пустая'.format(table_name))
    if flag == True:
        return name
    else: return None



if __name__ == '__main__':
    while True:
        for i in range(len(table_list)):
            dump_db(table_list[i])
            print('я всё. отпевайте.')
        for i in range(24):
            print('следующий дамп будет через {} временев'.format(24-i))
            sleep(3600)