from time import time
import telebot
import xlrd
import random
from telebot.types import KeyboardButton, Message, ReplyKeyboardMarkup
import datetime

#Бот
key = open('key')
bot = telebot.TeleBot(key.read())
book = xlrd.open_workbook_xls('raspisanie.xls')
sheettime = book.sheet_by_index(3)
sheetanekdot = book.sheet_by_index(4)
key.close()

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


def mainraspisanie(group_type, today):
    raspisanie = str(today.time())
    group = book.sheet_by_index(group_type)
    days = ['  ПН\n','  ВТ\n','  СР\n','  ЧТВ\n','  ПТН\n']
    if group_type == 0:
        raspisanie += '  ТЕХ'
    elif group_type == 1:
        raspisanie += '  УН'
    else:
        raspisanie += '  Е/Н'

    if today.time() < datetime.time(15,15,0): # Если день уже прошёл
        weekday = today.weekday()
    else:
        weekday = today.weekday() + 1

    if (weekday == 6) or (weekday == 5): # Если выходные
        weekday = 0

    raspisanie += str(days[weekday])

    for i in range(1,7):
        raspisanie += str(group.cell_value(weekday, i))
        starttime = datetime.time(*xlrd.xldate_as_tuple(sheettime.cell_value(0,i), book.datemode)[3:])
        finishtime = datetime.time(*xlrd.xldate_as_tuple(sheettime.cell_value(1,i), book.datemode)[3:])
        try:
            peremenatime = datetime.time(*xlrd.xldate_as_tuple(sheettime.cell_value(0,i+1), book.datemode)[3:])
            if starttime < today.time() < finishtime:
                raspisanie += ' <-- Вы здесь'
            elif finishtime < today.time() < peremenatime:
                raspisanie += ' <-- Перемена'
        except IndexError:
            print('ок')

        raspisanie += '\n'

    return raspisanie

def getanekdot():
    rand = random.randrange(0,9)
    anekdot = sheetanekdot.cell_value(rand, 0)
    return anekdot

@bot.message_handler(commands=['start', 'help'])
def start_message(Message):
    bot.send_message(Message.chat.id, 'Добро пожаловать в бота c расписанием! \nСначала будьте добры указать свою группу.', reply_markup=menu)

@bot.message_handler(content_types=['text'])
def menuchoose(Message):
    text = Message.text
    date = datetime.datetime.fromtimestamp(Message.date)
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
            answer = mainraspisanie(global_group_type,date)
            bot.send_message(Message.chat.id, answer, reply_markup=menu)

        else:
            bot.send_message(Message.chat.id, 'группу то сначала выбери!!!', reply_markup=choose)

    elif text == 'Анекдот':
        bot.send_message(Message.chat.id, getanekdot(), reply_markup=menu)

    elif text == 'О нас':
        bot.send_message(Message.chat.id, 'Идейный вдохновитель: Виталя \nРеализация: Руслан\n Отдельное спасибо всем за идеи и усовершенстования ❤️ \nЕсли есть идеи или даже функциональные решения. \nПрошу писать мне лично или выложить решение на гитхаб: https://github.com/Landesh/botustelegramus', reply_markup=menu)

    else:
        bot.send_message(Message.chat.id, 'нихуя не понятно', reply_markup=menu)

    if datetime.datetime.fromtimestamp(Message.date) != date:
        bot.edit_message_text(Message.chat.id, 'ХАХА ИЗМЕНИЛ')


bot.polling(none_stop = True)
