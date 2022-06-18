import telebot
from telebot import types
import DATABASE 
import user_class
from datetime import date
import re

tmp_data = None
new_purchase = ()

with open("token_bot.txt", "r") as file:
    token_bot = file.read()
bot = telebot.TeleBot(token_bot)

@bot.message_handler(commands=['help'])
def print_help(message):
        bot.send_message(message.from_user.id, "/new - расскажи о своей покупке \n \
/change_category_name - сменить название категории\n \
/change_category_of_product - сменить категорию для продукта\n \
/delete_purchase - удаление покупки")
#обработка продукта, находит категорию или спрашивает пользователя
def processing_purchase(user_id, product, price):
    if user_class.check_user_category(user_id, product, price):
        bot.send_message(user_id, "мы нашли категорию для этого продукта")
        return
    else: 
        category_offers = DATABASE.category_statistics(product)
        if len(category_offers)>1:
            creating_survey_about_category (user_id, category_offers, product, price)
        else:
            global new_purchase
            new_purchase = (product, price) 
            msg = bot.send_message(user_id, 'назови категорию для продукта')
            bot.register_next_step_handler(msg, get_category_for_new_purchase)

def creating_survey_about_category (user_id, category_offersm, product, price):
    keyboard_categories = types.InlineKeyboardMarkup()  # наша клавиатура
    for cat in category_offers:
        key_knb = types.InlineKeyboardButton(text = cat, callback_data = cat)
        keyboard_new_bought.add(key_yes_knb)  # добавляем кнопку в клавиатуру
    key_idk = types.InlineKeyboardButton(text = 'другое..', callback_data = 0)
    keyboard_new_bought.add(key_idk)  # добавляем кнопку в клавиатуру
    question_knb = 'выбери категорию'
    bot.send_message(user_id, text=question_knb, reply_markup=keyboard_new_bought)
    @bot.callback_query_handler(func=lambda call: True)
    def query_handler(call):
        bot.answer_callback_query(user_id, text='Спасибо за ответ!')
        answer = ''
        if call.data != 0:
            print (call.data)
        #(user_id, category, product, price)
            user_class.add_to_category(user_id, call.data, product, price)
            bot.edit_message_reply_markup(user_id, call.message.message_id)
        else:  
            bot.edit_message_reply_markup(user_id, call.message.message_id)   
            global new_purchase 
            new_purchase = (product, price)                 
            msg = bot.send_message(user_id, 'назови свой вариант')
            bot.register_next_step_handler(msg, get_category_for_new_purchase)

#вызывается в случае отсутствия категории для продукта
def get_category_for_new_purchase(message):
    global new_purchase
    bot.send_message(message.from_user.id, 'Здорово! Что-то еще?')
    print_help(message)
    #(user_id, category, product, price)
    user_class.add_to_category(message.from_user.id, message.text, new_purchase[0], new_purchase[1])


#добавление новой покупки
@bot.message_handler(commands = ['new'])
def get_new_bought(message):
    bot.send_message(message.from_user.id, "Расскажи о покупке через пробел (цена вводится с точкой)")
    @bot.message_handler(content_types = "text")
    def get_bought(msg):
        user_id = message.from_user.id
        try:
            price = float(re.search(r'(\d|\.)+', msg.text).group(0))
        except:
            price = None
            bot.send_message(msg.from_user.id, "Кажется, ты ошибся в цене. Попробуй снова")
        try:
            product = (re.search(r'([А-яЁё]|[a-zA-Z])+', msg.text).group(0))
        except:
            product = None
            bot.send_message(msg.from_user.id, "Кажется, что-то не так с названием покупки. Попробуй снова")

        #Добиваюсь корректного ввода от пользователя
        if product!=None and price !=None:
                 bot.send_message(message.from_user.id, 
                 "Вот данные, что я получил:\n Цена: {} \n Название: {} ".format(str(price),product))
                 keyboard_new_bought = types.InlineKeyboardMarkup()  # наша клавиатура
                 key_yes_knb = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
                 keyboard_new_bought.add(key_yes_knb)  # добавляем кнопку в клавиатуру
                 key_no_knb = types.InlineKeyboardButton(text='Нет', callback_data='no')
                 keyboard_new_bought.add(key_no_knb)
                 question_knb = 'Верно?'
                 bot.send_message(message.from_user.id, text=question_knb, reply_markup=keyboard_new_bought)
                 global new_purchase
                 new_purchase = (product, price)
                 @bot.callback_query_handler(func=lambda call: True)
                 def query_handler(call):
                     bot.answer_callback_query(callback_query_id=call.id, text='Спасибо за ответ!')
                     answer = ''
                     if call.data == 'yes':
                        data = new_purchase
                        processing_purchase(message.from_user.id, data[0], data[1])
                     elif call.data == 'no':
                         answer = 'Попробуем снова?'                         
                         bot.send_message(call.message.chat.id, answer)
                     bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)

#позволяет получить статистику за определнный месяц
@bot.message_handler(commands = ['report_for_month'])
def report_for_month(message):
    id = message.from_user.id
    mesg = bot.send_message(id, "Напиши номер месяца, о котором хочешь узнать (статистика доступна за последний год)")
    bot.register_next_step_handler(mesg, get_statistics_for_month)
def get_statistics_for_month(mesg):
    try:
        print (DATABASE.month_money_statistics(mesg.from_user.id, int(mesg.text)))
    except:
        bot.send_message(id, "неверный ввод")
    
bot.message_handler(commands = ['report_for_period'])
def report_for_period(message):
    DATABASE.timecheck()
    id = message.from_user.id
    mesg = bot.send_message(id, "Напиши номер месяца, начиная с которого ты хочешь узнать статистику (статистика доступна за последний год)")
    bot.register_next_step_handler(mesg, get_statistics_for_period_one)

def get_statistics_for_period_one(mesg):
    global tmp_data
    tmp_data = mesg.text
    mesg = bot.send_message(id, "Напиши номер месяца - конец периода")
    bot.register_next_step_handler(mesg, get_statistics_for_period_two)

def get_statistics_for_period_two(mesg):
    global tmp_data
    try:
        print (DATABASE.year_money_statistics(mesg.from_user.id, int(tmp_data), int(mesg.text)))
    except:
        bot.send_message(id, "неверный ввод")

@bot.message_handler(commands = ['report_for_current_month'])
def report_for_current_month(message):
    DATABASE.timecheck()
    id = message.from_user.id
    print (DATABASE.current_month_money_statistics(id))

@bot.message_handler(commands = ['report_for_current_year'])
def report_for_current_year(message):
    DATABASE.timecheck()
    id = message.from_user.id
    print (DATABASE.year_money_statistics(id))

#позволяет менять название категории (последующие две функции вызываются цепочкой)
@bot.message_handler(commands = ['change_category_name'])
def change_category_name(message):
    old = bot.send_message(message.from_user.id, "имя какой категории нужно поменять?")
    bot.register_next_step_handler(old, get_old_category)

def get_old_category(msg):
    user_id = msg.from_user.id
    global tmp_data
    tmp_data = msg.text
    new = bot.send_message(msg.from_user.id, "на какую?")
    bot.register_next_step_handler(new, get_category_for_rename)

def get_category_for_rename(msg):
    global tmp_data    
    if user_class.change_category_name(msg.from_user.id, tmp_data, msg.text):
        bot.send_message(msg.from_user.id, 'Здорово! Что-то еще?')
        print_help(msg)
    else:
        bot.send_message(msg.from_user.id, 'такой категории нет')
        print_help(msg)
#позволяет менять категорию для продукта
@bot.message_handler(commands = ['change_category_of_product'])

def get_old_name_category(msg):
    user_id = msg.from_user.id
    new = bot.send_message(msg.from_user.id, "на какую категорию надо поменять?")
    bot.register_next_step_handler(new, get_new_name_category)

def get_new_name_category(msg):
    global tmp_data
    tmp_data = msg.text
    new = bot.send_message(msg.from_user.id, "какой продукт? (ответь на сообщение с покупкой чем твоей душе угодно)")
    bot.register_next_step_handler(new, get_name_for_rename)

def get_name_for_rename(msg):
    if msg.forward_from != None:
        try:
            price = float(re.search(r'(\d|\.)+', msg.text).group(0))
        except:
            price = None
            bot.send_message(msg.from_user.id, "Кажется, не подходит. Попробуй снова")
        try:
            product = (re.search(r'([А-яЁё]|[a-zA-Z])+', msg.text).group(0))
        except:
            product = None
            bot.send_message(msg.from_user.id, "Кажется, что-то не так с названием покупки. Попробуй снова")
        user_class.change_name_category(msg.from_user.id, price, product, tmp_data)
        bot.send_message(msg.from_user.id, "Отлично")
    elif msg.reply_to_message != None :
        try:
            price = float(re.search(r'(\d|\.)+', msg.reply_to_message.text).group(0))
        except:
            price = None
            bot.send_message(msg.from_user.id, "Кажется, это не подходит. Попробуй снова")
        try:
            product = (re.search(r'([А-яЁё]|[a-zA-Z])+', msg.reply_to_message.text).group(0))
        except:
            product = None
            bot.send_message(msg.from_user.id, "Кажется, что-то не так с названием покупки. Попробуй снова")
        user_class.change_name_category(msg.from_user.id, price, product, tmp_data)
        bot.send_message(msg.from_user.id, "Отлично")
    else:
        bot.send_message(msg.from_user.id, "Произошла ошибка. Попробуй снова")
    print_help(msg)

@bot.message_handler(commands = ['delete_purchase'])
def get_name_for_delete_purchase(message):
    purchase_delete = bot.send_message(message.from_user.id, "ответь на сообщение с покупкой чем твоей душе угодно")
    bot.register_next_step_handler(purchase_delete, deleting_purchase)
def deleting_purchase(msg):
    if msg.forward_from != None:
        try:
            price = float(re.search(r'(\d|\.)+', msg.text).group(0))
        except:
            price = None
            bot.send_message(msg.from_user.id, "Кажется, ты ошибся в цене. Попробуй снова")
        try:
            product = (re.search(r'([А-яЁё]|[a-zA-Z])+', msg.text).group(0))
        except:
            product = None
            bot.send_message(msg.from_user.id, "Кажется, что-то не так с названием покупки. Попробуй снова")

        DATABASE.delete_purchase(msg.from_user.id, product, price)
        bot.send_message(msg.from_user.id, "Отлично")
    elif msg.reply_to_message != None :
        try:
            price = float(re.search(r'(\d|\.)+', msg.reply_to_message.text).group(0))
        except:
            price = None
            bot.send_message(msg.from_user.id, "Кажется, ты ошибся в цене. Попробуй снова")
        try:
            product = (re.search(r'([А-яЁё]|[a-zA-Z])+', msg.reply_to_message.text).group(0))
        except:
            product = None
            bot.send_message(msg.from_user.id, "Кажется, что-то не так с названием покупки. Попробуй снова")

        bot.delete_message(msg.from_user.id, msg.reply_to_message.id)
        DATABASE.delete_purchase(msg.from_user.id, product, price)
        bot.send_message(msg.from_user.id, "Отлично")
    else:
        bot.send_message(msg.from_user.id, "Кажется, что-то не так. Попробуй снова")
    

DATABASE.timecheck()
bot.polling(none_stop=True, interval=0)
