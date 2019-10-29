# -*- coding: utf-8 -*-.
import telebot
from os import path, remove
import const_bot as const
from datetime import datetime
import codecs
import smtplib
import re
from email.mime.text import MIMEText
start = datetime.now()


bot = telebot.TeleBot(const.API_TOKEN)
print(bot.get_me())


def log(message):
    file = codecs.open("log/log.txt", "a", "cp1251")
    file.write("------------------------------------------------------------------\n")
    from datetime import datetime
    file.write("time : {0}\n".format(datetime.now()))
    print("Время : {0}\n".format(datetime.now()))
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    print(first_name, " ", last_name)
    try:
        file.write("first name :{0}\nlast name :{1}\n".format(first_name, last_name))
    except:
        try:
            file.write("last name :{0}\n".format(last_name))
        except:
            try:
                file.write("first name :{0}\n".format(first_name))
            except:
                pass
    file.write("id :(id={0})\n".format(str(message.from_user.id)))
    file.write("message text :{0}\n".format(message.text))
    file.close()

@bot.message_handler(commands=["start"])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False, None, 1)
    user_markup.add("пробить")
    bot.send_message(message.from_user.id, "хотите пробить человека?\nВы пришли по адресу!\n"
                                         , reply_markup=user_markup)


@bot.message_handler(content_types=['contact'])
def contact_handler(message):
    data = ''
    if path.isfile("./data/" + str(message.from_user.id) + ".txt"):
        file = codecs.open("./data/" + str(message.from_user.id) + ".txt", "r", "cp1251")
        data = file.read()
        file.close()
    file = codecs.open("./data/" + str(message.from_user.id) + ".txt", "w", "cp1251")
    file.write(data + message.contact.phone_number + "\n")
    file.close()
    bot.send_message(message.from_user.id, "также укажите пожалуйста свою почту gmail")


def start_markup(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False, None, 1)
    user_markup.add("пробить")
    bot.send_message(message.from_user.id, "если вы хотите заказать кого-то еще, нажмите кнопку \"пробить\""
                                         , reply_markup=user_markup)


def get_contact(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    reg_button = telebot.types.KeyboardButton(text="добавить телефон к заказу",
                                      request_contact=True)
    keyboard.add(reg_button)
    bot.send_message(message.chat.id, "оставтье пожалуйста свой номер телефона"
                                    , reply_markup=keyboard)


def send_mail(message):
    order_data = codecs.open("./data/" + str(message.from_user.id) + ".txt", "r", "cp1251").read()

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465

    MAIL_USERNAME = "shadowbot225@gmail.com"
    MAIL_PASSWORD = "shadow_bot_312"

    FROM = MAIL_USERNAME
    TO = 'shadowbot225@gmail.com'

    msg = order_data
    msg = MIMEText('\n {}'.format(msg).encode('utf-8'), _charset='utf-8')

    smtp_obj = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
    smtp_obj.ehlo()
    smtp_obj.login(MAIL_USERNAME, MAIL_PASSWORD)

    smtp_obj.sendmail(FROM, TO, 'Subject: id:{0} \n{1}'.format(message.from_user.id, msg))
    smtp_obj.quit()

    remove("./data/" + str(message.from_user.id) + ".txt")

    bot.send_message(message.chat.id, "спасибо, ваш заказ принят, ожидайте")

    start_markup(message)

    print("sending mail...")


@bot.message_handler(content_types=['text'])
def main_handle(message):
    log(message)
    if message.text == "пробить":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, row_width=1)
        user_markup.row("отправить данные")
        bot.send_message(message.chat.id, "укажите пожалуйста некоторые данные и мы сможем начать.\n"
                                          "от вас требуется номер или почта жертвы а так-же ими и фамилия "
                                          "в обязательном порядке\nтакже просим по возможности просим "
                                          "предоставить отчество жертвы или другие данные которые "
                                          "у вас имеются", reply_markup=user_markup)
    elif "@" in message.text:
        
        try:
            mail = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b', message.text)
            data = ''
            if path.isfile("./data/" + str(message.from_user.id) + ".txt"):
                file = codecs.open("./data/" + str(message.from_user.id) + ".txt", "r", "cp1251")
                data = file.read()
                file.close()
            file = codecs.open("./data/" + str(message.from_user.id) + ".txt", "w", "cp1251")
            file.write(data + mail[0] + "\n")
            file.close()
            send_mail(message)
        except:
            bot.send_message(message.chat.id, "укажите пожалуйста правильный адрес почты")

    else:
        if len(message.text) < 25:
            user_markup = telebot.types.ReplyKeyboardMarkup(True, row_width=1)
            user_markup.row("отправить данные еще раз")
            bot.send_message(message.chat.id, "вы указали слишком мало информации, повторите пожалуйста отправку данных"
                             , reply_markup=user_markup)
        else:
            file = codecs.open("./data/" + str(message.from_user.id) + ".txt", "w", "cp1251")
            file.write(message.text + "\n")
            file.close()
            get_contact(message)


print(datetime.now() - start)
bot.polling(none_stop=True, interval=2)
