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
                                    money_spent INTEGER NOT NULL);'''

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

def insert_new_category(data_tuple):
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        sqlite_insert_A = """INSERT INTO A_DATABASE
                              (word, category, frequency)
                              VALUES (?, ?, ?);"""
        sqlite_insert_B = """INSERT INTO B_DATABASE
                              (id, category, money_spent)
                              VALUES (?, ?, ?);"""
        sqlite_insert_C = """INSERT INTO C_DATABASE
                              (id, word, category)
                              VALUES (?, ?, ?);"""

        data_A = (data_tuple[2], data_tuple[1], 1)
        data_B = (data_tuple[0], data_tuple[1], data_tuple[3])
        data_C = (data_tuple[0], data_tuple[2], data_tuple[1])

        cursor.execute(sqlite_insert_A, data_A)
        cursor.execute(sqlite_insert_B, data_B)
        cursor.execute(sqlite_insert_C, data_C)
        sqlite_connection.commit()

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке Insertion: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def payment(data):
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        money_selection = """select money_spent from B_DATABASE where id = ? AND category = ?"""
        cursor.execute(money_selection, (data[0], data[1],))
        record = cursor.fetchall()
        money = record[0][0]

        sql_update_query = """Update B_DATABASE set money_spent = ? where id = ? and category = ?"""
        money += data[2]
        data = (money, data[0], data[1])
        cursor.execute(sql_update_query, data)
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке payment: ", error)
    finally:
        if sqlite_connection:
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

def delete_user(id):
    try:
        sqlite_connection = sqlite3.connect('DATABASE.db')
        cursor = sqlite_connection.cursor()

        sql_update_query = """DELETE from C_DATABASE where id = ?"""
        cursor.execute(sql_update_query, (id, ))
        sqlite_connection.commit()
        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка в блоке delete_user: ", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

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


if __name__ == "__main__":
    #data = (123, 'фрукты', 'банан', 200)
    #insert_new_category(data)

    data = (123, 'фрукты', 500)
    payment(data)