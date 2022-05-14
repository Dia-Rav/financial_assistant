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

def check_user_category(data):
    #data = (user_id (число), продукт (строка), price)
    #если мы уже создали этот объект, ищет объект в users_in_contact, иначе создает объект
    #ищет элемент в категориях
    current_user = users_in_contact.get(data[0], user(data[0]))
    categories = current_user.categories
    for key, products in categories.items():
        if data[1] in products:
            data1 = (data[0], key, data[2])
            print (data1)
            #data1= (id, category, price)
            DATABASE.payment(data1)
            return True
    return False

def change_category_name(data):
    #data = (id, название старой категории, название новой категории)
    current_user = users_in_contact.get(data[0], user(data[0]))
    current_id = data[0]
    old_category = data[1]
    new_category_text = data[2]
    if old_category in current_user.categories:
        data1 = (current_id, old_category, new_category_text, current_user.categories)
        DATABASE.change_category_name_DATABASE(data1)
        current_user.categories[new_category_text] = current_user.categories[old_category]
        del current_user.categories[old_category]
        return True
    else:
        return False
def change_name_category(data):
    #Входные данные data = (id, слово, название старой категории, название новой категории)
    current_user = users_in_contact.get(data[0], user(data[0]))
    current_id = data[0]
    print (data)
    old_category = data[2]
    new_category_text = data[3]
    print(current_user.categories)
    purchase = data[1]
    if old_category in current_user.categories:
        products = current_user.categories[old_category]
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
        DATABASE.change_name_category_DATABASE(data)
    else:
        current_user.categories[old_category] = (purchase)
        data_2 = (current_id, new_category_text, purchase, 0)
        new_category(data_2)


def new_category(data):#data = (user_id, категория, продукт, цена)
    #если мы уже создали этот объект, ищет объект в users_in_contact, иначе создает объект
    current_user = users_in_contact.get(data[0], user(data[0]))
    print (data)
    current_user.categories[data[1]] = (data[2])
    DATABASE.insert_new_category(data)
    return

def add_to_category(data):
    current_user = users_in_contact.get(data[0], user(data[0]))
    if data[1] in current_user.categories:
        products = current_user.categories[data[1]]
        current_user.categories[data[1]] = []
        for product in products:
            current_user.categories[data[1]].append(product)
        current_user.categories[data[1]] = tuple(current_user.categories[data[1]])
        DATABASE.add_product_at_category(data)
        pass 
    else:
        new_category(data)

#


number_of_days_monthly = [31, 28, 31, 30, 31, 30 ,31, 31, 30, 31, 30, 31]

