import telebot
from telebot import types
with open("token_bot.txt", "r") as file:
    token_bot = file.read()
bot = telebot.TeleBot(token_bot)
@bot.message_handler(commands=['help'])
def get_text_messages(message):
        bot.send_message(message.from_user.id, "Привет, я твой финансовый помощник. А ниже функции, "
                                               "которые я могу выполнять.\n ")
        bot.send_message(message.from_user.id, r"/new - расскажи о своей покупке")


@bot.message_handler(commands = ['new'])
def get_text_message(message):
    bot.send_message(message.from_user.id, "Расскажи о покупке в формате: категория цена название")\

    @bot.message_handler(content_types = "text")
    def get_category(msg):
        user_id = message.from_user.id
        new_bought = [user_id]
        new_bought_tmp = msg.text.split()
        #Добиваюсь корректного ввода от пользователя
        if len(new_bought_tmp) != 3: #Ввел не по шаблону
            new_bought_tmp = []
            bot.send_message(message.from_user.id, "Что-то тут не так. Давай еще раз")
        else:  #Ввел по шаблону, обрабатываю списки вида ["(str,"; "int,"; "str)"]
                                          #и списки с любыми перестановками символов ","; "()"
            #Проверка категории
            # if new_bought_tmp[0][0] == "(":
            #     new_bought_tmp[0] = new_bought_tmp[0][1:]
            # if new_bought_tmp[0][len(new_bought_tmp[0])-1] == ",":
            #     new_bought_tmp[0] = new_bought_tmp[0][:-1]
            print(new_bought_tmp[0])
            #Проверка цены
            # if new_bought_tmp[1][len(new_bought_tmp[1])-1] == ",":
            #     new_bought_tmp[1] = new_bought_tmp[1][:-1]
            print(new_bought_tmp[1])
            try:
                new_bought_tmp[1] = float(new_bought_tmp[1])  # Вместо цены какой-то бред
            except:
                new_bought_tmp = []
                bot.send_message(message.from_user.id, "Кажется, ты ошибся в цене. Попробуй снова")

            #Проверка названия
            # if new_bought_tmp[2][len(new_bought_tmp[2]) - 1] == ")":
            #         new_bought_tmp[2] = new_bought_tmp[2][:-1]
            try:
                print(new_bought_tmp[2])
            except:
                pass
            #if type(new_bought_tmp[2]) is int:  # Вместо названия какой-то бред
                #new_bought_tmp = []
                #bot.send_message(message.from_user.id, "Кажется, ты ошибся в категории. Попробуй снова")
            if new_bought_tmp:
                 new_bought.extend(new_bought_tmp)
                 bot.send_message(message.from_user.id, 
                 "Вот данные, что я получил:\n Категория: {} \n Цена: {} \n Название: {} ".format(new_bought[1],
                                                        str(new_bought[2]),
                                                        new_bought[3]))
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
                         answer = 'Здорово! Что-то еще?'
                     elif call.data == 'no':
                         answer = 'Попробуем снова?'

                     bot.send_message(call.message.chat.id, answer)
                     bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
               #После положительного ансвера отправим в основноем меню как в начале
bot.polling(none_stop=True, interval=0)
