import DATABASE
from datetime import date
import re
import itertools
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
    def get_user_id(self):
        return self.user_id

def new_payment(user_id, product, price):
    try:
        #(user_id (число), продукт (строка), price)
        #если мы уже создали этот объект, ищет объект в users_in_contact, иначе создает объект
        #ищет элемент в категориях
        current_user = users_in_contact.get(user_id, user(user_id))
        categories = current_user.categories
        for key, products in categories.items():
            if product in products:
                DATABASE.payment(user_id, key, price)
                return True
        return False
    except Exception as error:
        print ('ошибка в user_class.new_payment', repr(error))

def delete_cetegory(id, cat):
    current_user = users_in_contact.get(user_id, user(user_id))
    categories = current_user.categories
    try:
        if cat in categories:
            DATABASE.delete_cat()
            del current_user.categories[cat]
            return True
        else:
            return False
    except Exception as error :
        print ('ошибка в user_class.delete_cetegory', repr(error))


def change_category_name(user_id, old_category, new_category_text):
    try:
        #data = (id, название старой категории, название новой категории)
        current_user = users_in_contact.get(user_id, user(user_id))
        if old_category in current_user.categories:
            if new_category_text not in current_user.categories:
                current_user.categories[new_category_text] = current_user.categories[old_category]
                DATABASE.change_category_name_DATABASE(user_id, old_category, new_category_text, list(current_user.categories[old_category]), flag = 0)
            else:
                print (1)
                list_1 = list(current_user.categories[old_category])
                list_2 = list(current_user.categories[new_category_text])
                current_user.categories[new_category_text] = list(itertools.chain(list_1, list_2))
                DATABASE.change_category_name_DATABASE(user_id, old_category, new_category_text, list(current_user.categories[old_category]), flag = 1)
            del current_user.categories[old_category]
            return True
        else:
            return False
    except Exception as error:
        print ('ошибка в user_class.change_category_nam', repr(error))

def change_name_category(user_id, price, product, new_category_text):
    try:
        current_user = users_in_contact.get(user_id, user(user_id))
        old_category = None
        for cat, products in current_user.categories.items():
            if product in products:
                old_category = cat
        if new_category_text in current_user.categories:
            other_products = current_user.categories[new_category_text]
        else:
            other_products = ()
        current_user.categories[new_category_text] = []
        for y in other_products:
            current_user.categories[new_category_text].append(y)
        current_user.categories[new_category_text].append([product])
        #data = (id, слово, название старой категории, название новой категории, цена)
        DATABASE.change_name_category_DATABASE(user_id, product, old_category, new_category_text, price)
    except Exception as error:
        print ('ошибка в user_class.change_name_category', repr(error))


def new_category(user_id, category, product, price):#(user_id, категория, продукт, цена)
    try:
        #если мы уже создали этот объект, ищет объект в users_in_contact, иначе создает объект
        current_user = users_in_contact.get(user_id, user(user_id))
        current_user.categories[category] = (product)
        DATABASE.insert_new_category(user_id, category, product, price)
        return
    except Exception as error:
        print ('ошибка в user_class.new_category', repr(error))
#если объявленная категория для нового товара есть, то добавляется товар в статистику
#если тако категории нет, то создается
def add_to_category(user_id, category, product, price):
    try:
        current_user = users_in_contact.get(user_id, user(user_id))
        if category in current_user.categories:
            products = current_user.categories[category]
            current_user.categories[category] = []
            for prod in products:
                current_user.categories[category].append(prod)
            current_user.categories[category] = current_user.categories[category]
            DATABASE.add_product_to_category(user_id, category, product, price)
            pass 
        else:
            new_category(user_id, category, product, price)
    except Exception as error:
        print ('ошибка в user_class.add_to_category', repr(error))
    
number_of_days_monthly = [31, 28, 31, 30, 31, 30 ,31, 31, 30, 31, 30, 31]