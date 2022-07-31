import paramiko
import telebot

from telebot import types

bot = telebot.TeleBot('xxx')

command = "ssh_script.ssh"

host = "vps_ip"
username = "vps_username"
password = "pwd"


def generate():
    client = paramiko.client.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, username=username, password=password)
    _stdin, _stdout, _stderr = client.exec_command("ssh_script.sh")
    return(_stdout.read().decode())
    client.close()

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('ℹ️О проекте')
    item2 = types.KeyboardButton('💸 Помочь проекту')
    item3 = types.KeyboardButton('🛡️ А это безопасно?')
    item4 = types.KeyboardButton('🔑 Хочу ключик!')

    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, 'Привет! Этот бот выдает ключи для shadowsocks-сервиса Outline, который базируется на моем сервере.' .format(message.from_user), reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == 'ℹ️О проекте':
            bot.send_message(message.chat.id, 'Это маленький Outline-сервер для друзей. Outline можно загрузить на iOS и Android. Есть версии и для ПК. Сервер довольно быстрый, потому что на нем сидит не очень много юзеров. Физически сервер расположен в Латвии, где не очень принято блокировать «неудобные» ресурсы. Если у вас возникнут проблемы со скоростью подключения или сервер упадет — пишите прямо мне. Попробуем порешать.')
        elif message.text == '💸 Помочь проекту':
            bot.send_message(message.chat.id, 'Это некоммерческий проект, поэтому я не принимаю донаты. Если вам хочется меня отблагодарить, отправьте донат любой правозащитной организации по вашему вкусу — например, Агоре, ОВД-Инфо или Насилию.нет. Еще круто будет поддержать Медиазону или Медузу.')
        elif message.text == '🛡️ А это безопасно?':
            bot.send_message(message.chat.id, 'Теоретически да. Трафик шифруется уникальным ключом, который вам как раз и выдает этот бот. Если ключ попадет к товарищу майору, он сможет расшифровать ваш трафик. В принципе, провайдер может заметить подозрительно большой объем трафика, уходящий на один адрес, и заблочить мой сервер, но это маловероятно: он слишком маленький. И да, все это не значит, что можно качать детскую порнографию. Пожалуйста, не делайте этого.')
        elif message.text == '🔑 Хочу ключик!':
            bot.send_message(message.chat.id, text = str(generate()))
bot.delete_webhook()
bot.polling()
