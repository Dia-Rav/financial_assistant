class user:
    def __init__ (self, id, date_of_start = 1):
        #дата начала, чтобы, например, мы могли выдавать статистику за прошлые месяцы
        #(пока поставим начало месяца, но в будущем это, например, может быт день зп)
        self.user_id = id 
        self.date_of_start = date_of_start
        self.categories = get_dict(id)
        users_is_contact[id] = self
        return self
        #информация должна приходить от тг бота
    def change_name(self, new_name):
        self.user_name = new_name
    def get_user_name (self):
        return self.user_name
    def get_user_id(self):
        return self.user_id
    #метод для сохранения объекта
    # def save(self):
    #     return (self.__class__, self.__dict__)
    

def check_user_category(data):
    #data = (user_id (число), продукт (строка), цена (число))
    #если мы уже создали этот объект, ищет объект в users_in_contact, иначе создает объект
    current_user = users_in_contact.get(data[0], user(data[0]))
    categories = current_user.categories
    for key, products in categories.items():
        if data[1] in products:
            data1 = (data[0], key, data[2])
            payment(data1)
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
        change_category_name_DATABASE(data1)
        current_user.categories[current_new_category] = current_user.categories[current_old_category]
        del current_user.categories[current_old_category]
        return True
    else:
        return False


def new_category(new_data):#new_data = (user_id, категория, продукт, цена)
    #если мы уже создали этот объект, ищет объект в users_in_contact, иначе создает объект
    current_user = users_in_contact.get(data[0], user(data[0]))
    current_user.categories[data[1]] = (data[2])
    insert_new_category(new_data)
    return


# def load(cls, attributes):
#     obj = cls.__new__(cls)  # Создание объекта класса cls без вызова __init__
#     obj.__dict__.update(attributes)  # Добавление в объект десериализованных атрибутов
#     return obj

# id_123 = user('Diana', 123)
# id_123.categories = {'food': ('eggs', 'milk', 'apples'), 'drinks': ('tea', 'coffee')}
# data = (id_123, 'coffee', 256)

users_in_contact = {}