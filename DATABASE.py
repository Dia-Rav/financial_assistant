import sqlite3

def create_database_A():
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        sqlite_create_table_query = '''CREATE TABLE A_DATABASE (
                                    word TEXT NOT NULL,
                                    category TEXT NOT NULL,
                                    frequency INTEGER NOT NULL);'''

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица статистики по категориям A_DATABASE создана")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке Creation_A: ", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()

def create_database_B():
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        sqlite_create_table_query = '''CREATE TABLE B_DATABASE (
                                    id INTEGER NOT NULL,
                                    category TEXT NOT NULL,
                                    money_spent INTEGER NOT NULL,
                                    last_change_month INTEGER NOT NULL);'''

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица финансов B_DATABASE создана")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке Creation_B: ", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()

def create_database_C():
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        sqlite_create_table_query = '''CREATE TABLE C_DATABASE (
                                    id INTEGER NOT NULL,
                                    word TEXT NOT NULL,
                                    category TEXT NOT NULL);'''

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица категорий пользователей C_DATABASE создана")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке Creation_C: ", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()

def create_database_STATISTICS():
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        sqlite_create_table_query = '''CREATE TABLE STATISTICS (
                                    id INTEGER NOT NULL,
                                    category TEXT NOT NULL,
                                    money_spent INTEGER NOT NULL,
                                    month INTEGER NOT NULL);'''

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица трат по месяцам STATISTICS создана")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке Creation_STATISTICS: ", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()

def A_update(data_A, cursor, sqlite_connection):
    try:
        check_existance = """select word from A_DATABASE where word = ? AND category = ?"""
        cursor.execute(check_existance, data_A)
        record = cursor.fetchall()
        if record == []:
            sqlite_insert_A = """INSERT INTO A_DATABASE
                                    (word, category, frequency)
                                    VALUES (?, ?, ?);"""
            data_A = (data_A[0], data_A[1], 1)
            cursor.execute(sqlite_insert_A, data_A)
            sqlite_connection.commit()
        else:
            sqlite_insert_A = """Update A_DATABASE set frequency = frequency + 1 where word = ? AND category = ?"""
            cursor.execute(sqlite_insert_A, data_A)
            sqlite_connection.commit()
    except sqlite3.Error as error:
        print("Ошибка в блоке A_update: ", error)

def B_update(data_B, cursor, sqlite_connection): #data_B = (id, category, money)
    try:
        check_existance = """select category from B_DATABASE where id = ? AND category = ?"""
        cursor.execute(check_existance, (data_B[0], data_B[1]))
        record = cursor.fetchall()
        if record == []:
            sqlite_insert_B = """INSERT INTO B_DATABASE
                              (id, category, money_spent, last_change_month)
                              VALUES (?, ?, ?, ?);"""
            data_B = (data_B[0], data_B[1], data_B[2], month_today(cursor, sqlite_connection))
            cursor.execute(sqlite_insert_B, data_B)
            sqlite_connection.commit()
        else:
            payment(data_B, 0, cursor, sqlite_connection)
    except sqlite3.Error as error:
        print("Ошибка в блоке B_update: ", error)

def insert_new_category(data_tuple):   #data = (user_id, категория, продукт, цена)
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()
        
        sqlite_insert_C = """INSERT INTO C_DATABASE
                              (id, word, category)
                              VALUES (?, ?, ?);"""
        data_C = (data_tuple[0], data_tuple[2], data_tuple[1])

        cursor.execute(sqlite_insert_C, data_C)
        sqlite_connection.commit()

        data_A = (data_tuple[2], data_tuple[1])
        A_update(data_A, cursor, sqlite_connection)

        data_B = (data_tuple[0], data_tuple[1], data_tuple[3])
        B_update(data_B, cursor, sqlite_connection)

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке Insertion: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def add_product_to_category(data_tuple):   #data = (user_id, категория, продукт, цена)
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()
        
        sqlite_insert_C = """INSERT INTO C_DATABASE
                              (id, word, category)
                              VALUES (?, ?, ?);"""

        data_C = (data_tuple[0], data_tuple[2], data_tuple[1])

        cursor.execute(sqlite_insert_C, data_C)
        sqlite_connection.commit()


        data_A = (data_tuple[2], data_tuple[1])
        A_update(data_A, cursor, sqlite_connection)

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке Insertion: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
        payment((data_tuple[0], data_tuple[1], data_tuple[3]))

def change_category_name_DATABASE(data):
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        sql_update_query = """Update B_DATABASE set category = ? where id = ? AND category = ?"""
        update_data = (data[2], data[0], data[1])
        cursor.execute(sql_update_query, update_data)
        sqlite_connection.commit()

        sql_update_query = """Update C_DATABASE set category = ? where id = ? AND category = ?"""
        cursor.execute(sql_update_query, update_data)
        sqlite_connection.commit()
        
        words_to_update = []
        for word in data[3]:                                   #создаём список слов для обновления которые переходят из старой категории (data[1]) в новую (data[2])
            words_to_update.append((data[1], word))
        
        sql_update_query = """Update A_DATABASE set frequency = frequency - 1 where category = ? AND word = ?"""
        cursor.executemany(sql_update_query, words_to_update)                                                     #понижаем частоту слов, так как у них поменялась категория
        sqlite_connection.commit()

        cleaning(cursor, sqlite_connection) #чистим таблицу от нулевых частот

        for word in data[3]:                         #обновление статистики по новой категории 
            A_update((word, data[2]), cursor, sqlite_connection)
        
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка в блоке change_category_name_DATABASE: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def change_name_category_DATABASE(data): #data = (id, слово, название старой категории, название новой категории)
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        sql_update_query = """Update C_DATABASE set category = ? where id = ? AND word = ?"""
        cursor.execute(sql_update_query, (data[3], data[0], data[1]))
        sqlite_connection.commit()
        
        words_to_update = [(data[2], data[1])]
        
        sql_update_query = """Update A_DATABASE set frequency = frequency - 1 where category = ? AND word = ?"""
        cursor.executemany(sql_update_query, words_to_update)                                                     #понижаем частоту слова, так как у него поменялась категория
        sqlite_connection.commit()

        cleaning(cursor, sqlite_connection) #чистим таблицу от нулевых частот

        A_update((data[1], data[3]), cursor, sqlite_connection)        #обновление статистики по новой категории 
        
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка в блоке change_category_name_DATABASE: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def payment(data, flag = 1, cursor = 0, sqlite_connection = 0): #data1 = (user_id, категория, цена)
    try:
        if flag == 1:
            sqlite_connection = sqlite3.connect('DATABASE.db')
            cursor = sqlite_connection.cursor()

        money_selection = """select money_spent from B_DATABASE where id = ? AND category = ?"""
        cursor.execute(money_selection, (data[0], data[1],))
        record = cursor.fetchall()
        money = record[0][0]

        sql_update_query = """Update B_DATABASE set money_spent = ?, last_change_month = ? where id = ? and category = ?"""
        money += data[2]
        update_data = (money, month_today(cursor, sqlite_connection), data[0], data[1])
        cursor.execute(sql_update_query, update_data)
        sqlite_connection.commit()
        if flag == 1:
            cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке payment: ", error)
    finally:
        if flag == 1 and sqlite_connection:
            sqlite_connection.close()

def get_dict(id):
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        user_dict = dict()
        sql_select_query = """select word, category from C_DATABASE where id = ?"""
        cursor.execute(sql_select_query, (id,))
        records = cursor.fetchall()
        for row in records:
            if row[1] not in user_dict.keys():
                user_dict[row[1]] = set()
            user_dict[row[1]].add(row[0])
        
        return user_dict
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке get_dict: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def update_category(id, category_to_update, new_category):
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        sql_update_query = """Update C_DATABASE set category = ? where id = ? and category = ?"""
        data = (new_category, id, category_to_update)
        cursor.execute(sql_update_query, data)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке update_category: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def timecheck():
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        current_month = month_today(cursor, sqlite_connection)

        sql_select_query = """SELECT id FROM B_DATABASE where last_change_month = ?"""
        cursor.execute(sql_select_query, (current_month,))
        records = cursor.fetchall()
        if records == []:
            sql_select_query = """SELECT * FROM B_DATABASE"""
            cursor.execute(sql_select_query)
            records = cursor.fetchall()
            for row in records:
                check_existance = """select id from STATISTICS where id = ? and category = ? and month = ?"""
                cursor.execute(check_existance, (row[0], row[1], row[3], ))
                record = cursor.fetchall()
                if record == []:
                    sqlite_insert_STATISTICS = """INSERT INTO STATISTICS
                                        (id, category, money_spent, month)
                                        VALUES (?, ?, ?, ?);"""
                    data = (row[0], row[1], row[2], row[3])

                    cursor.execute(sqlite_insert_STATISTICS, data)
                    sqlite_connection.commit()
                else:
                    sqlite_update_STATISTICS = """Update STATISTICS set money_spent = ? where id = ? and category = ? and month = ?"""
                    data = (row[2], row[0], row[1], row[3])
                    cursor.execute(sqlite_update_STATISTICS, data)
                    sqlite_connection.commit()

            sqlite_update_B = """Update B_DATABASE set money_spent = 0 """
            cursor.execute(sqlite_update_B)
            sqlite_connection.commit()
        
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке timecheck: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def otchet():
     try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        table = 'База данных по статистике\n \nслово\t\tкатегория\tчастота \n'

        sql_select_query = """SELECT * FROM A_DATABASE"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()

        for row in records:
            tmp = str(row[0]) + '\t\t' + str(row[1]) + '\t\t' + str(row[2]) + '\n'
            table += tmp

        table += '\nБаза данных по денежным тратам\n \nid\t\tкатегория\tпотраченные деньги \n'

        sql_select_query = """SELECT * FROM B_DATABASE"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()

        for row in records:
            tmp = str(row[0]) + '\t' + str(row[1]) + '\t\t' + str(row[2]) + '\t\t' + str(row[3]) + '\n'
            table += tmp

        table += '\nБаза данных по статистике\n \nid\t\tслово\t\tкатегория \n'

        sql_select_query = """SELECT * FROM C_DATABASE"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()

        for row in records:
            tmp = str(row[0]) + '\t' + str(row[1]) + '\t\t' + str(row[2]) + '\n'
            table += tmp

        print(table)
        cursor.close()

     except sqlite3.Error as error:
        print("Ошибка в блоке otchet: ", error)
     finally:
        if sqlite_connection:
            sqlite_connection.close()

def delete_user(id):
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        sql_delete_query = """DELETE from B_DATABASE where id = ?"""
        cursor.execute(sql_delete_query, (id, ))
        sqlite_connection.commit()
        sql_delete_query = """DELETE from C_DATABASE where id = ?"""
        cursor.execute(sql_delete_query, (id, ))
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке delete_user: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def cleaning(cursor, sqlite_connection):
    try:
        sql_delete_query = """DELETE from A_DATABASE where frequency = 0"""
        cursor.execute(sql_delete_query)
        sqlite_connection.commit()

    except sqlite3.Error as error:
        print("Ошибка в блоке cleaning: ", error)

def delete_ALL():
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        A = """DELETE FROM A_DATABASE"""
        B = """DELETE FROM B_DATABASE"""
        C = """DELETE FROM C_DATABASE"""
        cursor.execute(A)
        cursor.execute(B)
        cursor.execute(C)
        sqlite_connection.commit()
        print("ВСЕ записи успешно удалены")
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке delete_ALL: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def month_today(cursor, sqlite_connection):
    try:
        month = """SELECT strftime('%m', 'now')"""
        cursor.execute(month)
        records = cursor.fetchall()
        return(int(records[0][0]))

    except sqlite3.Error as error:
        print("Ошибка в блоке month_today: ", error)
        if sqlite_connection:
            sqlite_connection.close()

def check():
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        chk = """SELECT strftime('%m', 'now')"""
        cursor.execute(chk)
        records = cursor.fetchall()

        print(records[0][0])
        print('Done!')
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке check: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

if __name__ == '__main__':
    timecheck()