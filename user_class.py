import DATABASE
from datetime import date

users_in_contact = {}

class user:
    def __init__ (self, id, date_of_start = 1):
        #дата начала, чтобы, например, мы могли выдавать статистику за прошлые месяцы
        #(пока поставим начало месяца, но в будущем это, например, может быт день зп)
        self.user_id = id 
        self.date_of_start = date_of_start
        self.categories = DATABASE.get_dict(id)
        global users_in_contact
        users_in_contact[id]  = self
        return
        #информация должна приходить от тг бота
    def change_name(self, new_name):
        self.user_name = new_name
    def get_user_name (self):
        return self.user_name
    def get_user_id(self):
        return self.user_id

def check_user_category(data):
    #data = (user_id (число), продукт (строка), price)
    #если мы уже создали этот объект, ищет объект в users_in_contact, иначе создает объект
    current_user = users_in_contact.get(data[0], user(data[0]))
    categories = current_user.categories
    for key, products in categories.items():
        if data[1] in products:
            data1 = (data[0], key, data[2])
            print (data1)
            DATABASE.payment(data1)
            return True
    return False

def change_category_name(data):
    #data = (id, название старой категории, название новой категории)
    current_user = users_in_contact.get(data[0], user(data[0]))
    current_id = data[0]
    current_old_category = data[1]
    current_new_category = data[2]
    if current_old_category in current_user.categories:
        data1 = (current_id, current_old_category, current_new_category, current_user.categories)
        DATABASE.change_category_name_DATABASE(data1)
        current_user.categories[current_new_category] = current_user.categories[current_old_category]
        del current_user.categories[current_old_category]
        return True
    else:
        return False
def change_name_category(data):
    #Входные данные data = (id, слово, название старой категории, название новой категории)
    current_user = users_in_contact.get(data[0], user(data[0]))
    current_id = data[0]
    current_old_category = data[2]
    current_new_category = data[3]
    current_purchase = data[1]
    if current_old_category in current_user.categories:
        current_user.categories[current_old_category]
        current_user.categories[current_new_category] = (current_purchase)
        DATABASE.change_name_category_DATABASE(data)

    else:
        current_user.categories[current_old_category] = (current_purchase)
        new_category((current_id, current_new_category, current_purchase, 0))

def new_category(data):#data = (user_id, категория, продукт, цена)
    #если мы уже создали этот объект, ищет объект в users_in_contact, иначе создает объект
    current_user = users_in_contact.get(data[0], user(data[0]))
    print (data)
    current_user.categories[data[1]] = (data[2])
    DATABASE.insert_new_category(data)
    return



number_of_days_monthly = [31, 28, 31, 30, 31, 30 ,31, 31, 30, 31, 30, 31]

