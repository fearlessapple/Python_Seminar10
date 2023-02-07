from fractions import Fraction
import datetime     
import telebot      
from telebot import types

bot = telebot.TeleBot("5655871385:AAHa46r4R5db0R-C4Wg9LqkdCZiSJNL1cIU")

@bot.message_handler(commands = ["button", "start"])
def button(message):
    print("/start")
    global calc, num_text, num, num1, num2, res, txt, text
    calc = 0        
    num_text = []   
    num = 0         
    text = ""
    txt = (f"{datetime.datetime.now()},{message.from_user.username},{message.from_user.first_name},{message.from_user.last_name}")
    print("Запуск контроллера калькулятора")
    bot.send_message(message.chat.id,"Калькулятор для работы с рациональными и комплексными числами")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Калькулятор: рациональные числа")
    but2 = types.KeyboardButton("Калькулятор: комплексные числа")
    markup.add(but1)
    markup.add(but2)
    bot.send_message(message.chat.id, "Выбери тип чисел: рациональные или комплексные", reply_markup=markup)


def input_frac_number(num_text):
    print("-- обработка рационального числа")
    num_text = list(map(int,num_text))
    frac = Fraction(num_text[0], num_text[1])
    print(frac)
    return(frac)


def input_complex_number(num_text):
    print("-- обработка комплексного числа")
    num_text = list(map(float,num_text))
    compl = complex(num_text[0], num_text[1])
    print(compl)
    return(compl)

def summ(message, num1, num2):
    res = num1 + num2
    bot.send_message(message.chat.id,"Сумма: "+str(res))
    bot.send_message(message.chat.id,"Перезапустите калькулятор /start")
    log_calc(num1, num2, res)


def diff(message, num1, num2):
    res = num1 - num2
    bot.send_message(message.chat.id,"Разница: "+str(res))
    bot.send_message(message.chat.id,"Перезапустите калькулятор /start")
    log_calc(num1, num2, res)


def mult(message, num1, num2):
    res = num1 * num2
    bot.send_message(message.chat.id,"Произведение: "+str(res))
    bot.send_message(message.chat.id,"Перезапустите калькулятор /start")
    log_calc(num1, num2, res)


def div(message, num1, num2):
    res = num1 / num2
    bot.send_message(message.chat.id,"Деление: "+str(res))
    bot.send_message(message.chat.id,"Перезапустите калькулятор /start")
    log_calc(num1, num2, res)


def int_div(message, num1, num2):
    res = num1 // num2
    bot.send_message(message.chat.id,"Целочисленное деление: "+str(res))
    bot.send_message(message.chat.id,"Перезапустите калькулятор /start")
    log_calc(num1, num2, res)


def rem_div(message, num1, num2):
    res = num1 % num2
    bot.send_message(message.chat.id,"Остаток от деление: "+str(res))
    bot.send_message(message.chat.id,str(res))
    bot.send_message(message.chat.id,"Перезапустите калькулятор /start")
    log_calc(num1, num2, res)


def input_num(message, num_text):
    if num_text[0].isdigit and num_text[1].isdigit:
        global calc, num1, num2, num
        print("введены два числа через разделитель: обаботка...")
        if num == 0:
            if calc == 1:
                num1 = input_frac_number(num_text)
            if calc == 2:
                num1 = input_complex_number(num_text)
            num = 1
            bot.send_message(message.chat.id,"Введите второе число:")
        elif num == 1:
            if calc == 1:
                num2 = input_frac_number(num_text)
                operation_frac(message)
            if calc == 2:
                num2 = input_complex_number(num_text)
                operation_complex(message)
            num = 2
        else: bot.send_message(message.chat.id,"Нужно выбрать операцию над числами")


def log_calc(num1, num2, res):
    global txt, text
    txt = txt + (f",{num1},{num2},{text},") + str(res)
    print(txt)
    file = open("log_calc.csv", "a", encoding='utf-8')
    file.write(f"{txt}\n")
    file.close()
    print("файл записан")


@bot.message_handler(content_types=["text"])
def controller (message):
    global calc, num_text, num, num1, num2, txt, text
    text = message.text
    if text == "Калькулятор: рациональные числа":
        calc = 1  
        txt = txt + ",рациональные числа"
        print("Вводим рациональные числа")
        bot.send_message(message.chat.id,"Введите два рациональных числа вида (m/n)")
        if num == 0:
            bot.send_message(message.chat.id,"* сначала Числитель (m - целое число), затем через символ '/', Знаменатель (n - действительное число)")
            bot.send_message(message.chat.id,"Введите первое число:")
    if text == "Калькулятор: комплексные числа":
        calc = 2 
        txt = txt + ",комплексные числа"
        print("Вводим комплексные числа")
        bot.send_message(message.chat.id,"Введите два комплексных числа вида (a + b*j)")
        if num == 0:
            bot.send_message(message.chat.id,"* сначала (a), затем через пробел, (b)")
            bot.send_message(message.chat.id,"Введите первое число:")

    if calc == 1:
        if text.find("/"): num_text = text.split("/")
        if len(num_text) == 2: input_num(message, num_text)
        if text == "Сложение (+)":
            summ(message, num1, num2)
        if text == "Вычитания (-)":
            diff(message, num1, num2)
        if text == "Умножение (х)":
            mult(message, num1, num2)
        if text == "Деление (/)":
            div(message, num1, num2)
        if text == "Целочисленное деление (//)":
            int_div(message, num1, num2)
        if text == "Остаток от деления (%)":
            rem_div(message, num1, num2)

    if calc == 2:
        if text.find(" "): num_text = text.split(" ")
        if len(num_text) == 2: input_num(message, num_text)
        if text == "Сложение (+)":
            summ(message, num1, num2)
        if text == "Вычитания (-)":
            diff(message, num1, num2)
        if text == "Умножение (х)":
            mult(message, num1, num2)
        if text == "Деление (/)":
            div(message, num1, num2)

def operation_frac(message):
    print("Запуск контроллера операций с Рациональными числами")
    bot.send_message(message.chat.id,"Действия с рациональными числами")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Сложение (+)")
    but2 = types.KeyboardButton("Вычитания (-)")
    but3 = types.KeyboardButton("Умножение (х)")
    but4 = types.KeyboardButton("Деление (/)")
    but5 = types.KeyboardButton("Целочисленное деление (//)")
    but6 = types.KeyboardButton("Остаток от деления (%)")
    markup.add(but1)
    markup.add(but2)
    markup.add(but3)
    markup.add(but4)
    markup.add(but5)
    markup.add(but6)
    bot.send_message(message.chat.id, "Выбери тип операции:", reply_markup=markup)

def operation_complex(message):
    print("Запуск контроллера операций с Комплексными числами")
    bot.send_message(message.chat.id,"Действия с комплексными числами")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton("Сложение (+)")
    but2 = types.KeyboardButton("Вычитания (-)")
    but3 = types.KeyboardButton("Умножение (х)")
    but4 = types.KeyboardButton("Деление (/)")
    markup.add(but1)
    markup.add(but2)
    markup.add(but3)
    markup.add(but4)
    bot.send_message(message.chat.id, "Выбери тип операции:", reply_markup=markup)

print("ЗАПУСК")
bot.infinity_polling()