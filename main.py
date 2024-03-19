import telebot
from telebot import types
import yaml

with open('conf.yaml', "r") as yamlfile:
    config = yaml.load(yamlfile, Loader=yaml.FullLoader)
    print("Read config successful")

# Telegram
BOT_TOKEN = config['telegram']['BOT_TOKEN']
ADMIN_ID = config['telegram']['ADMIN_ID']

# TODO поставить токен бота
bot = telebot.TeleBot(BOT_TOKEN)
waiting_for_text = {}
waiting_for_question = {}
waiting_for_mark = {}
waiting_for_text_1 = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Задать вопрос')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Написать отзыв')
    btn3 = types.KeyboardButton('Оценить')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, f'Здравствуйте, <b>{message.from_user.first_name}!</b> \nДанный бот поможет держать обратную связь с разработчиками.\n'
                                      f'\nНиже можете скачать последнюю версию приложения.', parse_mode='html', reply_markup=markup)
    file = open('fin_assistant.apk', 'rb')
    bot.send_document(message.chat.id, file)


@bot.message_handler(func=lambda message: message.text in ['Написать отзыв'], content_types=['text'])
def handle_choice(message):
    waiting_for_text[message.chat.id] = True

    bot.send_message(message.chat.id, "Отправьте ваш отзыв.")


@bot.message_handler(func=lambda message: waiting_for_text.get(message.chat.id), content_types=['text'])
def handle_review(message):
    global copied_message
    waiting_for_text[message.chat.id] = False
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Да')
    btn2 = types.KeyboardButton('Нет')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('Назад')
    markup.row(btn3)
    copied_message = message.text
    bot.send_message(message.chat.id, 'Вы уверены, что хотите отправить данный отзыв?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Да'], content_types=['text'])
def yes(message):
    global name
    global id
    global username
    name = message.from_user.first_name
    id = message.from_user.id
    username = message.from_user.username or "Не установлен"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Задать вопрос')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Написать отзыв')
    btn3 = types.KeyboardButton('Оценить')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, "Cпасибо за отзыв.", reply_markup=markup)
    # TODO вставить свой ID
    bot.send_message( ADMIN_ID , f'Новый отзыв\nИмя: {name} \nID: {id} \nUsername: @{username}\nОтзыв: {copied_message}')


@bot.message_handler(func=lambda message: message.text in ['Нет'], content_types=['text'])
def no(message):
    waiting_for_text[message.chat.id] = True
    bot.send_message(message.chat.id, "Исправьте ваш отзыв.")


@bot.message_handler(func=lambda message: waiting_for_text.get(message.chat.id), content_types=['text'])
def no_1(message):
    waiting_for_text[message.chat.id] = False
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Да')
    btn2 = types.KeyboardButton('Нет')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Вы уверены, что хотите отправить данный отзыв?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Назад'], content_types=['text'])
def back(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Задать вопрос')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Написать отзыв')
    btn3 = types.KeyboardButton('Оценить')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, 'Главное меню:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Задать вопрос'], content_types=['text'])
def question(message):
    waiting_for_question[message.chat.id] = True
    bot.send_message(message.chat.id, 'Напишите свой вопрос и он будет перенаправлен разработчику.')


@bot.message_handler(func=lambda message: waiting_for_question.get(message.chat.id), content_types=['text'])
def question_1(message):
    global copied_question
    waiting_for_question[message.chat.id] = False
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Да, хочу')
    btn2 = types.KeyboardButton('Нет, не хочу')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('Назад')
    markup.row(btn3)
    copied_question = message.text
    bot.send_message(message.chat.id, 'Вы уверены, что хотите задать этот вопрос?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Да, хочу'], content_types=['text'])
def yes_2(message):
    global name_question
    global id_question
    global username_question
    name_question = message.from_user.first_name
    id_question = message.from_user.id
    username_question = message.from_user.username or "Не установлен"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Задать вопрос')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Написать отзыв')
    btn3 = types.KeyboardButton('Оценить')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, "В скором времени разработчик Вам ответит.", reply_markup=markup)
    # TODO вставить свой ID
    bot.send_message( ADMIN_ID , f'Новый вопрос\nИмя: {name_question} \nID: {id_question} \nUsername: @{username_question}\nОтзыв: {copied_question}')


@bot.message_handler(func=lambda message: message.text in ['Нет, не хочу'], content_types=['text'])
def no_3(message):
    waiting_for_question[message.chat.id] = True
    bot.send_message(message.chat.id, "Исправьте ваш вопрос.")


@bot.message_handler(func=lambda message: waiting_for_text.get(message.chat.id), content_types=['text'])
def no_4(message):
    waiting_for_question[message.chat.id] = False
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Да, хочу')
    btn2 = types.KeyboardButton('Нет, не хочу')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Вы уверены, что хотите задать этот вопрос?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Оценить'], content_types=['text'])
def ocenka(message):
    global name_mark
    global id_mark
    global username_mark
    name_mark = message.from_user.first_name
    id_mark = message.from_user.id
    username_mark = message.from_user.username or "Не установлен"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('1')
    btn2 = types.KeyboardButton('2')
    btn3 = types.KeyboardButton('3')
    btn4 = types.KeyboardButton('4')
    btn5 = types.KeyboardButton('5')
    markup.row(btn1, btn2, btn3, btn4, btn5)
    btn6 = types.KeyboardButton('6')
    btn7 = types.KeyboardButton('7')
    btn8 = types.KeyboardButton('8')
    btn9 = types.KeyboardButton('9')
    btn10 = types.KeyboardButton('10')
    markup.row(btn6, btn7, btn8, btn9, btn10)
    btn11 = types.KeyboardButton('Назад')
    markup.row(btn11)
    bot.send_message(message.chat.id, 'Оцените наше приложение, по 10-ти балльной шкале, предложенной ниже.', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['1', '2', '3', '4'], content_types=['text'])
def ploho(message):
    global copied_mark
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Рассказать')
    btn2 = types.KeyboardButton('Воздержаться')
    markup.add(btn1, btn2)
    copied_mark = message.text
    bot.send_message(message.chat.id, 'Можете рассказать, что Вам не понравилось в приложении?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['5', '6', '7',], content_types=['text'])
def norm(message):
    global copied_mark
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Рассказать')
    btn2 = types.KeyboardButton('Воздержаться')
    markup.add(btn1, btn2)
    copied_mark = message.text
    bot.send_message(message.chat.id, 'Можете рассказать, как мы можем улучшить приложение?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['8', '9', '10',], content_types=['text'])
def top(message):
    global copied_mark
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Рассказать')
    btn2 = types.KeyboardButton('Воздержаться')
    markup.add(btn1, btn2)
    copied_mark = message.text
    bot.send_message(message.chat.id, 'Можете рассказать, чем вам понравилось приложение?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Воздержаться'], content_types=['text'])
def rasskaz_no(message):
    global name_no
    global id_no
    global username_no
    name_no = message.from_user.first_name
    id_no = message.from_user.id
    username_no = message.from_user.username or "Не установлен"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Задать вопрос')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Написать отзыв')
    btn3 = types.KeyboardButton('Оценить')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, 'Хорошо, Вы будете направлены в главное меню.', reply_markup=markup)
    # TODO вставить свой ID
    bot.send_message(ADMIN_ID, f'Новая оценка\nИмя: {name_no} \nID: {id_no} \nUsername: @{username_no}\nОценка: {copied_mark}\nОтзыв: отсутствует')


@bot.message_handler(func=lambda message: message.text in ['Рассказать'], content_types=['text'])
def handle_choice_1(message):
    waiting_for_text_1[message.chat.id] = True
    bot.send_message(message.chat.id, "Отправьте ваш отзыв.")


@bot.message_handler(func=lambda message: waiting_for_text_1.get(message.chat.id), content_types=['text'])
def handle_review_1(message):
    global copied_message_1
    waiting_for_text_1[message.chat.id] = False
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Уверен')
    btn2 = types.KeyboardButton('Не уверен')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('Назад')
    markup.row(btn3)
    copied_message_1 = message.text
    bot.send_message(message.chat.id, 'Вы уверены, что хотите отправить данный отзыв?', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text in ['Уверен'], content_types=['text'])
def yes_mark(message):
    global name_mark
    global id_mark
    global username_mark
    name_mark = message.from_user.first_name
    id_mark = message.from_user.id
    username_mark = message.from_user.username or "Не установлен"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Задать вопрос')
    markup.row(btn1)
    btn2 = types.KeyboardButton('Написать отзыв')
    btn3 = types.KeyboardButton('Оценить')
    markup.row(btn2, btn3)
    bot.send_message(message.chat.id, "Cпасибо за отзыв.", reply_markup=markup)
    # TODO вставить свой ID
    bot.send_message( ADMIN_ID, f'Новая оценка\nИмя: {name_mark} \nID: {id_mark} \nUsername: @{username_mark}\nОценка: {copied_mark}\nОтзыв: {copied_message_1}')


@bot.message_handler(func=lambda message: message.text in ['Не уверен'], content_types=['text'])
def ne(message):
    waiting_for_text_1[message.chat.id] = True
    bot.send_message(message.chat.id, "Исправьте ваш отзыв.")


@bot.message_handler(func=lambda message: waiting_for_text.get(message.chat.id), content_types=['text'])
def ne_1(message):
    waiting_for_text_1[message.chat.id] = False
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('Уверен')
    btn2 = types.KeyboardButton('Не уверен')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Вы уверены, что хотите отправить данный отзыв?', reply_markup=markup)


bot.polling(none_stop=True)