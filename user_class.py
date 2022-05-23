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
    def get_user_id(self):
        return self.user_id

def check_user_category(user_id, product, price):
    #(user_id (число), продукт (строка), price)
    #если мы уже создали этот объект, ищет объект в users_in_contact, иначе создает объект
    #ищет элемент в категориях
    current_user = users_in_contact.get(user_id, user(user_id))
    categories = current_user.categories
    for key, products in categories.items():
        if product in products:
            data1 = (user_id, key, product, price)
            print (data1)
            DATABASE.payment(user_id, key, product, price)
            return True
    return False

def change_category_name(user_id, old_category, new_category_text):
    #data = (id, название старой категории, название новой категории)
    current_user = users_in_contact.get(user_id, user(user_id))
    if old_category in current_user.categories:
        DATABASE.change_category_name_DATABASE(user_id, old_category, new_category_text, list(current_user.categories[old_category]))
        current_user.categories[new_category_text] = current_user.categories[old_category]
        del current_user.categories[old_category]
        return True
    else:
        return False

def change_name_category(user_id, purchase, old_category, new_category_text):
    #Входные данные data = (id, слово, название старой категории, название новой категории)
    current_user = users_in_contact.get(user_id, user(user_id))
    if old_category in current_user.categories:
        products = list(current_user.categories[old_category])
        current_user.categories[old_category] = []
        for x in products:
            if x == purchase:
                if new_category_text in current_user.categories:
                    other_products = current_user.categories[new_category_text]
                    current_user.categories[new_category_text] = []
                    for y in other_products:
                        current_user.categories[new_category_text].append(y)
                else:
                    current_user.categories[new_category_text] = [purchase]
            else:
                current_user.categories[old_category].append(x)
        current_user.categories[new_category_text] = tuple(current_user.categories[new_category_text])
        current_user.categories[old_category] = tuple(current_user.categories[old_category])
        DATABASE.change_name_category_DATABASE(user_id, purchase, old_category, new_category_text)
    else:
        current_user.categories[old_category] = (purchase)
        new_category(current_id, new_category_text, purchase, 0)


def new_category(user_id, category, product, price):#(user_id, категория, продукт, цена)
    #если мы уже создали этот объект, ищет объект в users_in_contact, иначе создает объект
    current_user = users_in_contact.get(user_id, user(user_id))
    current_user.categories[category] = (product)
    DATABASE.insert_new_category(user_id, category, product, price)
    return

def add_to_category(user_id, category, product, price):
    current_user = users_in_contact.get(user_id, user(user_id))
    if category in current_user.categories:
        products = current_user.categories[category]
        current_user.categories[category] = []
        for prod in products:
            current_user.categories[category].append(prod)
        current_user.categories[category] = tuple(current_user.categories[category])
        DATABASE.add_product_at_category(user_id, category, product, price)
        pass 
    else:
        new_category(data)

#
number_of_days_monthly = [31, 28, 31, 30, 31, 30 ,31, 31, 30, 31, 30, 31]
DATABASE.otchet()