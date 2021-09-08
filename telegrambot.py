import telebot
import xlrd
import os
from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup
from datetime import datetime

#секс бот
key = open('key')
bot = telebot.TeleBot(key.read)

#определения
button_texnik = KeyboardButton('Техник')
button_universal = KeyboardButton('Универсал')
button_estev = KeyboardButton('Естесвенно-научник')
chosee_kb = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(button_texnik,button_universal,button_estev)

def print_raspisanie(group_type, today):
    raspisanie = ''
    book = xlrd.open_workbook_xls('raspisanie.xls')
    sheet = book.sheet_by_index(group_type)
    for i in range(7):
        raspisanie = str(raspisanie) + str(sheet.cell_value(today, i)) +'\n'

    return raspisanie


@bot.message_handler(commands=['start'])
def start_message(Message):
    bot.send_message(Message.chat.id, 'Добро пожаловать в бота c расписанием! \nСначала будьте добры указать свою группу.', reply_markup=chosee_kb)

@bot.message_handler(content_types=['text'])
def groupchose(Message):
    date = datetime.fromtimestamp(Message.date)
    today = date.weekday()
    text = Message.text
    if text =='Техник':
        group_type = 0
        answer = 'Вау... 🥵'
    elif text == 'Универсал':
        group_type = 1
        answer = 'Ясно... 🤢'
    elif text == 'Естесвенно-научник':
        group_type = 2
        answer = 'Ясно... 🤮'

    bot.send_message(Message.chat.id, answer)

    bot.send_message(Message.chat.id, 'Ладно, вот твоё расписание.')

    answer = str(date.date()) + '\n========================= \n' + print_raspisanie(group_type,today)

    bot.send_message(Message.chat.id, answer)



bot.polling(none_stop = True)
