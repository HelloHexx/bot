
import telebot
from telebot import types
import json

class zakaz(object):
    """description of class"""

    def __init__(self,type_t):
        """Constructor"""
        self.type_t = type_t
        self.value = 0
        self.phon_num = ""
        self.name=""
        pass
    def a_type(self,aType):
        self.type_t.append(aType)
    def set_value(self,val):
        self.value = val
    def set_phon_num(self,phone):
        self.phon_num = phone
    def set_name(self,name):
        self.name = name
    def get_type(self):
        return self.type_t
    def get_value(self):
        return self.value


tulpis_type = [ "🟩Зеленые", "🟨Желтые", "🌷Красные" ]
reply = "980196074"


bot = telebot.TeleBot("1460673027:AAHLVICOyeZl5t9UMutco2kcygD0xlEnoe4", parse_mode=None)
menu = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
empty_key = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
menu.add('Собрать заказ')
menu.add('/help')

#itembtn1 = types.KeyboardButton('Собрать заказ')


@bot.message_handler(commands=['start'])
def send_welcome(message):
	#bot.reply_to(message, "Привет! Я помогу тебе сделать заказ тюльпанов!")
	bot.send_message(message.chat.id,"Привет! Я помогу тебе сделать заказ тюльпанов!",reply_markup=menu)
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Собрать заказ":
        markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
        
        for n in tulpis_type:
            markup.add(n)
        markup.add("Хочу выбрать несколько цветов!")
        order = zakaz(list())
        bot.send_message(message.chat.id, "Выбери цвет!", reply_markup=markup)
        bot.register_next_step_handler(message,choo_color,order)
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши привет")
    else:
         bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")


def choo_color(message,order):
    text = message.text
    if text == "Хочу выбрать несколько цветов!":
        color = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
        for n in tulpis_type:
            color.add(n)
        color.add('Закончить')
        bot.send_message(message.from_user.id, "Выберите интересующие цвета:",reply_markup=color)
        bot.register_next_step_handler(message,multicolor,order)
    else:
        bot.send_message(message.from_user.id, "Укажите количество:")
        order.a_type(text)
        bot.register_next_step_handler(message,set_value,order)


        
def multicolor(message,order):
    text = message.text
    if text == 'Закончить':
        bot.send_message(message.from_user.id, "Выбранные цвета: " +str(order.get_type()))
        bot.send_message(message.from_user.id, "Укажите количество:",reply_markup=empty_key)
        bot.register_next_step_handler(message,set_value,order)
    else:
        order.a_type(text)
        bot.send_message(message.from_user.id, "Выбранные цвета: " +str(order.get_type()))
        bot.register_next_step_handler(message,multicolor,order)

def set_value(message,order):

    text = message.text
    if not text.isdigit():
        msg = bot.send_message(message.chat.id, 'Ответ должен быть числом, введите ещё раз.')
        bot.register_next_step_handler(msg, set_value,order) #askSource
    order.set_value(text)
    bot.send_message(message.chat.id,'Укажите ваше имя:')
    bot.register_next_step_handler(message, set_name,order)

def set_name(message,order):
    text = message.text
    order.set_name(text)
    bot.send_message(message.chat.id, 'Отлично! Теперь введите ваш номер телефона для связи с вами:')
    bot.register_next_step_handler(message, set_phon,order)

    

def set_phon(message,order):
    text = message.text
    order.set_phon_num(text)
    bot.send_message(reply,"Новый заказ.\nДетали: Выбранные цвета" + str(order.get_type()) + "\nКоличество: "+str(order.get_value())+"\nНомер телефона: "+ str(order.phon_num)+"\nИмя: "+ str(order.name))
    bot.send_message(message.chat.id,'Заказ оформлен! Детали: Выбранные цвета' + str(order.get_type()) + " Количество: "+str(order.get_value()) +" Номер телефона: "+ str(order.phon_num))
bot.polling(none_stop=True, interval=0)