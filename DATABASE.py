import sqlite3

def create_database_FREQUENCY():
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        sqlite_create_table_query = '''CREATE TABLE FREQUENCY (
                                    word TEXT NOT NULL,
                                    category TEXT NOT NULL,
                                    frequency INTEGER NOT NULL);'''

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица статистики по категориям FREQUENCY создана")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке Creation_FREQUENCY: ", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()

def create_database_MONEY():
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        sqlite_create_table_query = '''CREATE TABLE MONEY (
                                    id INTEGER NOT NULL,
                                    category TEXT NOT NULL,
                                    money_spent INTEGER NOT NULL,
                                    last_change_month INTEGER NOT NULL);'''

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица финансов MONEY создана")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке Creation_MONEY: ", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()

def create_database_WORDS_CATEGORIES():
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        sqlite_create_table_query = '''CREATE TABLE WORDS_CATEGORIES (
                                    id INTEGER NOT NULL,
                                    word TEXT NOT NULL,
                                    category TEXT NOT NULL);'''

        cursor = sqlite_connection.cursor()
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица категорий пользователей WORDS_CATEGORIES создана")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке Creation_WORDS_CATEGORIES: ", error)
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

def FREQUENCY_update(product, category, cursor, sqlite_connection):
    try:
        check_existance = """select word from FREQUENCY where word = ? AND category = ?"""
        cursor.execute(check_existance, (product, category))
        record = cursor.fetchall()
        if record == []:
            sqlite_insert_FREQUENCY = """INSERT INTO FREQUENCY
                                    (word, category, frequency)
                                    VALUES (?, ?, ?);"""
            cursor.execute(sqlite_insert_FREQUENCY, (product, category, 1))
            sqlite_connection.commit()
        else:
            sqlite_insert_FREQUENCY = """Update FREQUENCY set frequency = frequency + 1 where word = ? AND category = ?"""
            cursor.execute(sqlite_insert_FREQUENCY, (product, category))
            sqlite_connection.commit()
    except sqlite3.Error as error:
        print("Ошибка в блоке FREQUENCY_update: ", error)

def MONEY_update(user_id, category, price, cursor, sqlite_connection): #data_B = (id, category, money)
    try:
        check_existance = """select category from MONEY where id = ? AND category = ?"""
        cursor.execute(check_existance, (user_id, category))
        record = cursor.fetchall()
        if record == []:
            sqlite_insert_MONEY = """INSERT INTO MONEY
                              (id, category, money_spent, last_change_month)
                              VALUES (?, ?, ?, ?);"""
            cursor.execute(sqlite_insert_MONEY, (user_id, category, price, month_today(cursor, sqlite_connection)))
            sqlite_connection.commit()
        else:
            payment(user_id, category, price, 0, cursor, sqlite_connection)
    except sqlite3.Error as error:
        print("Ошибка в блоке MONEY_update: ", error)

def insert_new_category(user_id, category, product, price):   #data = (user_id, категория, продукт, цена)
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()
        
        sqlite_insert_WORDS_CATEGORIES = """INSERT INTO WORDS_CATEGORIES
                              (id, word, category)
                              VALUES (?, ?, ?);"""
        data_WORDS_CATEGORIES = (user_id, product, category)

        cursor.execute(sqlite_insert_WORDS_CATEGORIES, data_WORDS_CATEGORIES)
        sqlite_connection.commit()

        FREQUENCY_update(product, category, cursor, sqlite_connection)

        MONEY_update(user_id, category, price, cursor, sqlite_connection)

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке Insertion: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def add_product_to_category(user_id, category, product, price):   #data = (user_id, категория, продукт, цена)
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()
        
        sqlite_insert_WORDS_CATEGORIES = """INSERT INTO WORDS_CATEGORIES
                              (id, word, category)
                              VALUES (?, ?, ?);"""

        cursor.execute(sqlite_insert_WORDS_CATEGORIES, (user_id, product, category))
        sqlite_connection.commit()

        FREQUENCY_update(product, category, cursor, sqlite_connection)

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке Insertion: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
        payment(user_id, category, price)

def change_category_name_DATABASE(user_id, old_category, new_category, words):  #data1 = (id, название старой категории, название новой, список слов сменяемой категории)
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        MONEY_update_query = """Update MONEY set category = ? where id = ? AND category = ?"""
        cursor.execute(MONEY_update_query, (new_category, user_id, old_category))
        sqlite_connection.commit()

        WORDS_CATEGORIES_update_query = """Update WORDS_CATEGORIES set category = ? where id = ? AND category = ?"""
        cursor.execute(WORDS_CATEGORIES_update_query, (new_category, user_id, old_category))
        sqlite_connection.commit()
        
        words_to_update = []
        for word in words:                                   #создаём список слов для обновления которые переходят из старой категории в новую 
            words_to_update.append((old_category, word))
        
        FREQUENCY_update_query = """Update FREQUENCY set frequency = frequency - 1 where category = ? AND word = ?"""
        cursor.executemany(FREQUENCY_update_query, words_to_update)                                                     #понижаем частоту слов, так как у них поменялась категория
        sqlite_connection.commit()

        cleaning(cursor, sqlite_connection) #чистим таблицу от нулевых частот

        for word in words:                         #обновление статистики по новой категории 
            FREQUENCY_update(word, new_category, cursor, sqlite_connection)
        
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка в блоке change_category_name_DATABASE: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def change_name_category_DATABASE(user_id, word, old_category, new_category, price = 0): #data = (id, слово, название старой категории, название новой категории, цена)
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        WORDS_CATEGORIES_update_query = """Update WORDS_CATEGORIES set category = ? where id = ? AND word = ?"""
        cursor.execute(WORDS_CATEGORIES_update_query, (new_category, user_id, word))
        sqlite_connection.commit()
        
        MONEY_update(user_id, new_category, price, cursor, sqlite_connection)

        words_to_update = [(old_category, word)]
        
        FREQUENCY_update_query = """Update FREQUENCY set frequency = frequency - 1 where category = ? AND word = ?"""
        cursor.executemany(FREQUENCY_update_query, words_to_update)                                                     #понижаем частоту слова, так как у него поменялась категория
        sqlite_connection.commit()

        cleaning(cursor, sqlite_connection) #чистим таблицу от нулевых частот

        FREQUENCY_update(word, new_category, cursor, sqlite_connection)        #обновление статистики по новой категории 
        
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка в блоке change_category_name_DATABASE: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def payment(user_id, category, price, flag = 1, cursor = 0, sqlite_connection = 0): #data1 = (user_id, категория, цена)
    try:
        if flag == 1:
            sqlite_connection = sqlite3.connect('DATABASE.db')
            cursor = sqlite_connection.cursor()

        money_selection = """select money_spent from MONEY where id = ? AND category = ?"""
        cursor.execute(money_selection, (user_id, category,))
        record = cursor.fetchall()
        money = record[0][0]

        MONEY_update_query = """Update MONEY set money_spent = ?, last_change_month = ? where id = ? and category = ?"""
        money += price
        cursor.execute(MONEY_update_query, (money, month_today(cursor, sqlite_connection), user_id, category))
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
        WORDS_CATEGORIES_select_query = """select word, category from WORDS_CATEGORIES where id = ?"""
        cursor.execute(WORDS_CATEGORIES_select_query, (id,))
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

        WORDS_CATEGORIES_update_query = """Update WORDS_CATEGORIES set category = ? where id = ? and category = ?"""
        cursor.execute(WORDS_CATEGORIES_update_query, (new_category, id, category_to_update))
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

        MONEY_select_query = """SELECT id FROM MONEY where last_change_month = ?"""
        cursor.execute(MONEY_select_query, (current_month,))
        records = cursor.fetchall()
        if records == []:
            MONEY_select_query = """SELECT * FROM MONEY"""
            cursor.execute(MONEY_select_query)
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

            sqlite_update_MONEY = """Update MONEY set money_spent = ?, last_change_month = ?"""
            cursor.execute(sqlite_update_MONEY, (0, month_today(cursor, sqlite_connection, )))
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

        sql_select_query = """SELECT * FROM FREQUENCY"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()

        for row in records:
            tmp = str(row[0]) + '\t\t' + str(row[1]) + '\t\t' + str(row[2]) + '\n'
            table += tmp

        table += '\nБаза данных по денежным тратам\n \nid\t\tкатегория\tпотраченные деньги \n'

        sql_select_query = """SELECT * FROM MONEY"""
        cursor.execute(sql_select_query)
        records = cursor.fetchall()

        for row in records:
            tmp = str(row[0]) + '\t' + str(row[1]) + '\t\t' + str(row[2]) + '\t\t' + str(row[3]) + '\n'
            table += tmp

        table += '\nБаза данных по статистике\n \nid\t\tслово\t\tкатегория \n'

        sql_select_query = """SELECT * FROM WORDS_CATEGORIES"""
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

        sql_delete_query = """DELETE from MONEY where id = ?"""
        cursor.execute(sql_delete_query, (id, ))
        sqlite_connection.commit()
        sql_delete_query = """DELETE from WORDS_CATEGORIES where id = ?"""
        cursor.execute(sql_delete_query, (id, ))
        sqlite_connection.commit()
        sql_delete_query = """DELETE from STATISTICS where id = ?"""
        cursor.execute(sql_delete_query, (id, ))
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке delete_user: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def delete_purchase(user_id, product, price):
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        finding_category = """select category from WORDS_CATEGORIES where word = ? AND id = ?"""
        cursor.execute(finding_category, (product, user_id))
        record = cursor.fetchall()
        category = record[0][0]
        payment(user_id, category, -price, 0, cursor, sqlite_connection)

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке delete_purchase: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def cleaning(cursor, sqlite_connection):
    try:
        sql_delete_query = """DELETE from FREQUENCY where frequency = 0"""
        cursor.execute(sql_delete_query)
        sqlite_connection.commit()

    except sqlite3.Error as error:
        print("Ошибка в блоке cleaning: ", error)

def delete_ALL(flag = 1):
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        FREQUENCY = """DELETE FROM FREQUENCY"""
        MONEY = """DELETE FROM MONEY"""
        WORDS_CATEGORIES = """DELETE FROM WORDS_CATEGORIES"""
        STATISTICS = """DELETE FROM STATISTICS"""
        cursor.execute(FREQUENCY)
        cursor.execute(MONEY)
        cursor.execute(MONEY)
        if flag == 1:
            cursor.execute(STATISTICS)
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

def current_month_money_statistics(user_id):
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        MONEY_select_query = """select category, money_spent from MONEY where id = ?"""
        cursor.execute(MONEY_select_query, (user_id,))
        record = cursor.fetchall()
        cursor.close()
        return(record)
    except sqlite3.Error as error:
        print("Ошибка в блоке current_statistics: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def month_money_statistics(user_id, month):
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        STATISTICS_select_query = """select category, money_spent from STATISTICS where id = ? AND month = ?"""
        cursor.execute(STATISTICS_select_query, (user_id, month,))
        output = cursor.fetchall()
        cursor.close()
        if output == []:
            output = 0
        return(output)
    except sqlite3.Error as error:
        print("Ошибка в блоке current_statistics: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def category_statistics(word):
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        FREQUENCY_select_query = """select category, frequency from FREQUENCY where word = ?"""
        cursor.execute(FREQUENCY_select_query, (word,))
        record = cursor.fetchmany(3)
        record = sorted(record, key=lambda x: x[1], reverse=True)
        output = []
        for el in record:
            output.append(el[0])
        cursor.close()
        return(output)

    except sqlite3.Error as error:
        print("Ошибка в блоке current_statistics: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def year_money_statistics(user_id, start = 1, finish = 12):
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()
        output = dict()

        for month in range(start, finish):
            STATISTICS_select_query = """select category, money_spent from STATISTICS where id = ? AND month = ?"""
            cursor.execute(STATISTICS_select_query, (user_id, month,))
            record = cursor.fetchall()
            for word, money in record:
                if word in output:
                    output[word] += money
                else:
                    output[word] = money
        if output == {}:
            output = 0
        cursor.close()
        return(output)
    except sqlite3.Error as error:
        print("Ошибка в блоке current_statistics: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

if __name__ == '__main__':
    #print(year_money_statistics(999900000))
    pass
    #timecheck()
    #delete_purchase(999900000, 'bread', 100)
    #insert_new_category(999900000, 'food', 'bread', 100)
    #insert_new_category(999900000, 'food', 'apple', 50)
    #insert_new_category(999900000, 'drink', 'cola', 50)
    #insert_new_category(999911111, 'food', 'bread', 90)
    #insert_new_category(999911111, 'other', 'glue', 500)
    #insert_new_category(999911111, 'drink', 'milk', 80)