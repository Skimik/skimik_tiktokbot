import pymysql

class Database:
    ''' этот комментарий не совсем соответствует действительности. в действительности же я когда-то его перепишу и он будет ей соответствовать
        а пока, я, читающий свои же модуле после суток в визуалке и ничегошеньки не понимающий, возьми листочек, ручечку, выпиши задачи, идеи, таски                                                                               и пездуй спать, заебал
        и довольствуйся той действительностью, которая сама себе несоответствует

        класс содержит методы для работы с базой данных. полностью (в заданных рамках) настраивается (переписывается)
        описание методов:
        insert принимает на вход название_таблицы и значения в [values]. вставляет [values] в название_таблицы
        select ищет заданный столбец по заданному условию и выводит заданное количество результатов
        update обновляет заданное значение в заданном столбце по заданному условию
        delete удаляет запись из заданной таблицы по условию наличия в ней некоторых ячеек
        executor выполняет код, переданный в параметр sql. если тебе вдруг мало

    '''

    def __init__(self,
                    table_name,
                    database_host = '127.0.0.1',
                    database_user = 'root',
                    database_pass = '1234',
                    database_name = 'tiktok'
                    ):
        self.table_name = table_name
        self.connection = pymysql.connect(host      =database_host,
                                          user      =database_user,
                                          password  =database_pass,
                                          db        =database_name,
                                          charset   ='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)
#-------------------------------------------------------------------------------
    def insert_db(self, column=None, values=[]):
        #вставка значения в базу данных.
        ms_cursor=self.connection.cursor()
        #try:
        if column == None:
            sql = 'INSERT INTO {} VALUES ({});'

            ms_cursor.execute(sql.format(self.table_name, ', '.join(values)))
        else:
            sql = 'INSERT INTO {} ({}) VALUES ({});'
            ms_cursor.execute(sql.format(self.table_name, ', '.join(column), ', '.join(values)))
        self.connection.commit()
        self.connection.close()
        text = ''
        #except:
            #self.connection.close()
            #text = '--------------------------------------ошибка в функции insert_db'
            #print(text)

#-------------------------------------------------------------------------------
    def select_db(self, searched_column = 'id', condition = '', count_value = 0):
        #поиск наименования в таблице. выводит наличие элемента и результат поиска

        text = ''
        ms_cursor=self.connection.cursor()
        if True:
        #try:
            sql = "select {} from {} {};"
            
            available=ms_cursor.execute(sql.format( searched_column,
                                                    self.table_name,
                                                    condition))
            if count_value == 0:
                result=ms_cursor.fetchall()
            elif count_value >= 1:
                result=ms_cursor.fetchmany(count_value)
            else: print('ты совсем дурак? в select_db не может быть отрицательного вывода')
            self.connection.commit()
            self.connection.close()
            output={'available':available, 'result':result}
            text = 'у меня всё окей'
        #except:
        #    self.connection.close()
        #    text = '--------------------------------------ошибка в функции select_db'
        #    output={'available':None, 'result':None}
        #    print(text)
        return output

#-------------------------------------------------------------------------------
    def update_db(self, updated_column = 'id', updated_value = 'id', condition = ''):
        #обновление значений в базе данных по заданному условию
        text = ''
        ms_cursor=self.connection.cursor()
        try:
            sql = "update {} set {} = {} {};"
            ms_cursor.execute(sql.format(self.table_name,
                                         updated_column,
                                         updated_value,
                                         condition))
            self.connection.commit()
            self.connection.close()
        except Exception as ex:
            self.connection.close()
            text = '--------------------------------------ошибка в функции update_db'
            print(text+'\n'+str(ex))

    def delete_db(self, condition = ''):
        #удаление элементов базы данных

        text = ''
        ms_cursor=self.connection.cursor()
        try:
            # Create a new record
            sql = "delete from {} {};"
            ms_cursor.execute(sql.format(self.table_name,
                                         condition))
            self.connection.commit()
            self.connection.close()
            text = 'у меня всё окей'
        except:
            self.connection.close()
            text = '--------------------------------------ошибка в функции delete_db'
            print(text)

#-------------------------------------------------------------------------------
    def executor_db(self, sql):
        #универсальная функция обращения к базе данных. выполняет переданные ей команды в формате sql запросов
        ms_cursor=self.connection.cursor()
        ms_cursor.execute(sql)
        if sql.split(' ')[0].lower() == 'select':
            output = ms_cursor.fetchall()
        else:
            output = 'выхода нет или не найден'
        self.connection.commit()
        self.connection.close()
        return output
