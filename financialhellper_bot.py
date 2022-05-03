import telebot
from telebot import types
import user_class


with open("token_bot.txt", "r") as file:
    token_bot = file.read()
bot = telebot.AsyncTeleBot(token_bot)

@bot.message_handler(commands=['help'])
def print_help(message):
        bot.send_message(message.from_user.id, "Привет, я твой финансовый помощник. А ниже функции, "
                                               "которые я могу выполнять.\n ")
        bot.send_message(message.from_user.id, r"/new - расскажи о своей покупке")

def processing_purchase(data):
    if user_class.check_user_category(data):
        bot.send_message(data[0], "мы нашли категорию для этого продукта")
        return
    else: 
                            mesg = bot.send_message(data[0], "в какую категорию отнести этот продукт?")
                            bot.register_next_step_handler(mesg, get_category_for_new_purchase)

def get_category_for_new_purchase(message):
                                print ('я получил', massege)
                                new_data = (data[0], message, data[2], data[1])
                                user_class.new_category(new_data)

                                answer = 'Здорово! Что-то еще?'
                                bot.send_message(data[0], answer)
                                return



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
import asyncio
asyncio.run(bot.polling())


