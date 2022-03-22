class user:
    def __init__ (self, name, id, date_of_start = 1):
        #дата начала, чтобы, например, мы могли выдавать статистику за прошлые месяцы
        #(пока поставим начало месяца, но в будущем это, например, может быт день зп)
        self.user_name = name
        self.user_id = id 
        self.date_of_start = date_of_start
        self.categories = {}
        #информация должна приходить от тг бота
    def change_name(self, new_name):
        self.user_name = new_name
    def get_user_name (self):
        return self.user_name
    def get_user_id(self):
        return self.user_id
    #метод для сохранения объекта
    def save(self):
        return (self.__class__, self.__dict__)
    

def check_user_category(data):#data = (user_id (число), продукт (строка), цена (число))
    current_user = data[0]
    categories = current_user.categories
    for key, products in categories.items():
        print (products)
        if data[1] in products:
            data1 = (data[0], key, data[2])
            payment(data1)
            return True
    return False


def new_category(new_data):#new_data = (user_id, категория, продукт, цена)
    current_user = data[0]
    categories = current_user.categories
    categories[data[1]] = (data[2])
    insert_new_category(new_data)
    return


def load(cls, attributes):
    obj = cls.__new__(cls)  # Создание объекта класса cls без вызова __init__
    obj.__dict__.update(attributes)  # Добавление в объект десериализованных атрибутов
    return obj

# id_123 = user('Diana', 123)
# id_123.categories = {'food': ('eggs', 'milk', 'apples'), 'drinks': ('tea', 'coffee')}
# #надо по id воссаздовать объект 
# data = (id_123, 'coffee', 256)

def payment(data):
    pass