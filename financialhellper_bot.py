import telebot
from telebot import types
import DATABASE 
import user_class
import asyncio
tmp_data = None

new_category_in_func = None
with open("token_bot.txt", "r") as file:
    token_bot = file.read()
bot = telebot.TeleBot(token_bot)

@bot.message_handler(commands=['help'])
def print_help(message):
        bot.send_message(message.from_user.id, "Привет, я твой финансовый помощник. А ниже функции, "
                                               "которые я могу выполнять.\n ")
        bot.send_message(message.from_user.id, r"/new - расскажи о своей покупке")
        bot.send_message(message.from_user.id, r"/report_for_month - количество денег, потраченных за текущий месяц")
        bot.send_message(message.from_user.id, r"/report_for_year - количество денег, потраченных за текущий год")

def processing_purchase(data):
    if user_class.check_user_category(data):
        bot.send_message(data[0], "мы нашли категорию для этого продукта")
        return
    else: 
        global tmp_data 
        tmp_data = data
        mesg = bot.send_message(data[0], "в какую категорию отнести этот продукт?")
        bot.register_next_step_handler(mesg, get_category_for_new_purchase)


def get_category_for_new_purchase(message):
    global tmp_data
    answer = 'Здорово! Что-то еще?'
    bot.send_message(message.from_user.id, answer)
    data_all = (message.from_user.id, message.text, tmp_data[1], tmp_data[2])
    print (data_all)
    user_class.new_category(data_all)


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
        else:  #Ввел по шаблону, обрабатываю списки вида ["(str,"; "int,"; "str)"]
                                          #и списки с любыми перестановками символов ","; "()"

            print(new_bought_tmp[0])
            try:
                new_bought_tmp[0] = float(new_bought_tmp[0])  # Вместо цены какой-то бред
            except:
                new_bought_tmp = []
                bot.send_message(message.from_user.id, "Кажется, ты ошибся в цене. Попробуй снова")

            try:
                print(new_bought_tmp[1])
            except:
                pass

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
                 @bot.callback_query_handler(func=lambda call: True)
                 def query_handler(call):
                     bot.answer_callback_query(callback_query_id=call.id, text='Спасибо за ответ!')
                     answer = ''
                     if call.data == 'yes':
                        data = (new_bought[0], new_bought[2], new_bought[1])
                        processing_purchase(data)
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



bot.polling(none_stop=True, interval=0)




