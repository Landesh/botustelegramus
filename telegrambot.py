import telebot
import xlrd
from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup
from datetime import datetime

#секс бот
key = open('key.txt')
print(key.read())
bot = telebot.TeleBot('1996353008:AAFbmEF5glHEtp2VeBsb_kGhm7RwfU80CFM')

global_group_type = ''

#Клавиатуры
#первый выбор
button_texnik = KeyboardButton('Техник')
button_universal = KeyboardButton('Универсал')
button_estev = KeyboardButton('Естесвенно-научник')
choose = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(button_texnik,button_universal,button_estev)

#меню

button_choosegroup = KeyboardButton('Поменять группу')
button_raspisanie = KeyboardButton('Получить расписание')
button_danek = KeyboardButton('Анекдот')
button_aboutus = KeyboardButton('О нас')
menu = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(button_choosegroup).add(button_raspisanie).add(button_danek,button_aboutus)


def print_raspisanie(group_type, today):
    raspisanie = ''
    book = xlrd.open_workbook_xls('raspisanie.xls')
    sheet = book.sheet_by_index(group_type)
    for i in range(7):
        raspisanie = str(raspisanie) + str(sheet.cell_value(today, i)) +'\n'

    return raspisanie


@bot.message_handler(commands=['start', 'help'])
def start_message(Message):
    bot.send_message(Message.chat.id, 'Добро пожаловать в бота c расписанием! \nСначала будьте добры указать свою группу.', reply_markup=menu)

@bot.message_handler(content_types=['text'])
def menuchoose(Message):
    text = Message.text
    date = datetime.fromtimestamp(Message.date)
    today = date.weekday()
    global global_group_type 

    if text =='Поменять группу':
        bot.send_message(Message.chat.id, 'Выбирай.',reply_markup=choose)

    elif text =='Техник':
        global_group_type = 0
        bot.send_message(Message.chat.id, 'Вау... 🥵',reply_markup=menu)

    elif text == 'Универсал':
        global_group_type = 1
        bot.send_message(Message.chat.id, 'Ясно... 🤢',reply_markup=menu)

    elif text == 'Естесвенно-научник':
        global_group_type = 2
        bot.send_message(Message.chat.id, 'Ясно... 🤮',reply_markup=menu)

    elif text == 'Получить расписание':
        if type(global_group_type) == int:
            answer = str(date.date()) + '\n========================= \n' + print_raspisanie(global_group_type,today)
            bot.send_message(Message.chat.id, answer, reply_markup=menu)

        else:
            bot.send_message(Message.chat.id, 'группу то сначала выбери!!!', reply_markup=choose)

    elif text == 'Анекдот':
        bot.send_message(Message.chat.id, 'не работает сказал же', reply_markup=menu)
    elif text == 'О нас':
        bot.send_message(Message.chat.id, 'Идейный вдохновитель: виталька!!! \nЧел который все реализовал: руслан!!!\n Отдельное спасибо всем за идеи и усовершенстования ❤️ \nЕсли есть идеи или даже функциональные решения, прошу писать мне лично или выложить решение на гитхаб: https://github.com/Landesh/botustelegramus', reply_markup=menu)

    else:
        bot.send_message(Message.chat.id, 'нихуя не понятно', reply_markup=menu)


bot.polling(none_stop = True)
