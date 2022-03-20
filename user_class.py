class user:
    def __init__ (self, name, id, date_of_start = 1):
        #дата начала, чтобы, например мы могли выдавать статистику за прошлые месяцы
        #(пока поставим начало месяца, но в будущем это, например, может быт день зп)
        self.user_name = name
        self.user_id = id 
        self.date_of_start = date_of_start
        self.purchases_current_month = {}
        #информация должна приходить от тг бота
    def change_name(self, new_name):
        self.user_name = new_name
    def get_user_name (self):
        return self.user_name
    def get_user_id(self):
        return self.user_id

    #можно попробовать хранить информацию о покупках пользователя в его объекте
    def new_purchase (self, category, product_name, sum):
        if category in self.purchases_current_month:
            pass
    def next_month(self):
        pass
    def get_previous_month (self):
        pass
