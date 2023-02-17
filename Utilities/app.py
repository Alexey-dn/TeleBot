import telebot
from base_data import cur_list, TOKEN
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def greet(message: telebot.types.Message):
    text = f"Приветствую тебя, {message.chat.username}!\nЧтобы начать работу с телеботом\
    введите запрос через пробел:\n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\nесли есть вопросы жмите /help"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def hlp(message: telebot.types.Message):
    text = "Для просмотра всего списка валют выберете: /currency \n пример ввода запроса: доллар евро 100"
    bot.reply_to(message, text)

@bot.message_handler(commands=['currency'])
def value(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in cur_list.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")

        if len(values) != 3:
            raise ConvertionException("Слишком много параметров.")

        quote, base, amount = values
        total_base = CryptoConverter.errors_check(quote, base, amount)

    except ConvertionException as f:
        bot.reply_to(message, f"Ошибка пользователя\n {f}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n {e}")
    else:
        text = f"{total_base}"
        bot.send_message(message.chat.id, text)


bot.polling()