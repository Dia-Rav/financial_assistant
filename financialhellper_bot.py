import telebot
from telebot import types
import DATABASE 
import user_class
import asyncio
from datetime import date


tmp_data = None
new_purchase = ()

with open("token_bot.txt", "r") as file:
    token_bot = file.read()
bot = telebot.TeleBot(token_bot)

@bot.message_handler(commands=['help'])
def print_help(message):
        bot.send_message(message.from_user.id, "/new - расскажи о своей покупке \n \
/report_for_month - количество денег, потраченных за текущий месяц \n \
/report_for_year - количество денег, потраченных за текущий год \n \
/change_category_name - сменить название категории\n \
/change_name_category - сменить категорию для продукта")

def processing_purchase(user_id, product, price):
    if user_class.check_user_category(user_id, product, price):
        bot.send_message(user_id, "мы нашли категорию для этого продукта")
        print_help(user_id)
        return
    else: 
        global tmp_data 
        tmp_data = ((user_id, product, price))
        mesg = bot.send_message(user_id, "в какую категорию отнести этот продукт?")
        bot.register_next_step_handler(mesg, get_category_for_new_purchase)


def get_category_for_new_purchase(message):
    global tmp_data
    answer = 'Здорово! Что-то еще?'
    bot.send_message(message.from_user.id, answer)
    print_help(message)
    user_class.add_to_category(message.from_user.id, message.text, tmp_data[1], tmp_data[2])



@bot.message_handler(commands = ['new'])
def get_new_bought(message):
    bot.send_message(message.from_user.id, "Расскажи о покупке в формате: цена название")\

    @bot.message_handler(content_types = "text")
    def get_category(msg):
        user_id = message.from_user.id
        new_bought = [user_id]
        new_bought_tmp = msg.text.split()
        #Добиваюсь корректного ввода от пользователя
        if len(new_bought_tmp) != 2: #Ввел не по шаблону
            new_bought_tmp = []
            bot.send_message(message.from_user.id, "Что-то тут не так. Давай еще раз")
        else:  #Ввел по шаблону, обрабатываю списки вида [("int,"; "str)"]
            try:
                new_bought_tmp[0] = float(new_bought_tmp[0])  # Вместо цены какой-то бред
            except:
                new_bought_tmp = []
                bot.send_message(message.from_user.id, "Кажется, ты ошибся в цене. Попробуй снова")

            if new_bought_tmp:
                 new_bought.extend(new_bought_tmp)
                 bot.send_message(message.from_user.id, 
                 "Вот данные, что я получил:\n Цена: {} \n Название: {} ".format(str(new_bought[1]),
                                                        new_bought[2]))
                 keyboard_new_bought = types.InlineKeyboardMarkup()  # наша клавиатура
                 key_yes_knb = types.InlineKeyboardButton(text='Да', callback_data='yes')  # кнопка «Да»
                 keyboard_new_bought.add(key_yes_knb)  # добавляем кнопку в клавиатуру
                 key_no_knb = types.InlineKeyboardButton(text='Нет', callback_data='no')
                 keyboard_new_bought.add(key_no_knb)
                 question_knb = 'Верно?'
                 bot.send_message(message.from_user.id, text=question_knb, reply_markup=keyboard_new_bought)
                 global new_purchase
                 new_purchase = (new_bought[0], new_bought[2], new_bought[1])
                 @bot.callback_query_handler(func=lambda call: True)
                 def query_handler(call):
                     bot.answer_callback_query(callback_query_id=call.id, text='Спасибо за ответ!')
                     answer = ''
                     if call.data == 'yes':
                        data = new_purchase
                        processing_purchase(message.from_user.id, data[1], data[2])
                     elif call.data == 'no':
                         answer = 'Попробуем снова?'
                         
                         bot.send_message(call.message.chat.id, answer)
                     bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
                     


               #После положительного ансвера отправим в основноем меню как в начале

@bot.message_handler(commands = ['report_for_month'])
def report_for_month(message):
    id = message.from_user.id
    date_today = date.today()
    month_today = date_today.month
    year_today = date_today.year
    max_day = user_class.number_of_days_monthly[month_today-1]
    if month_today == 2 and year_today % 4 == 0 :
        max_day += 1
    date1 = date(year_today, month_today, 1)
    date2 = date(year_today, month_today, max_day)
    total = str(DATABASE.get_the_amount_period (id, date1, date2))
    bot.send_message(message.from_user.id, total)

@bot.message_handler(commands = ['report_for_year'])
def report_for_month(message):
    id = message.from_user.id
    date_today = date.today()
    year_today = date_today.year
    date1 = date(year_today, 1, 1)
    date2 = date(year_today, 12, 31)
    total = str(DATABASE.get_the_amount_period (id, date1, date2))
    bot.send_message(message.from_user.id, total)

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
        print_help(message)
    else:
        bot.send_message(msg.from_user.id, 'такой категории нет')
        print_help(msg)

@bot.message_handler(commands = ['change_name_category'])
def change_name_category(message):
    old = bot.send_message(message.from_user.id, "какую категории нужно поменять?")
    bot.register_next_step_handler(old, get_old_name_category)

def get_old_name_category(msg):
    user_id = msg.from_user.id
    global tmp_data
    tmp_data = [msg.text]
    new = bot.send_message(msg.from_user.id, "на какую?")
    bot.register_next_step_handler(new, get_new_name_category)

def get_new_name_category(msg):
    global tmp_data
    tmp_data.append (msg.text)
    new = bot.send_message(msg.from_user.id, "какой продукт?")
    bot.register_next_step_handler(new, get_name_for_rename)

def get_name_for_rename(msg):
    global tmp_data
    #data = (id, слово, название старой категории, название новой категории)
    bot.send_message(msg.from_user.id, "что-то еще?")
    user_class.change_name_category(msg.from_user.id, msg.text, tmp_data[0], tmp_data[1])


bot.polling(none_stop=True, interval=0)
DATABASE.timecheck()