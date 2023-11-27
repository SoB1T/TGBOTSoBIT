import telebot
from config import keys, TOKEN
from expections import ConvertExcept, CurrencyConvector

bot=telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start","help"])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите комманду боту в следующем формате:\n <имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \
Чтобы увидеть доступные к переводу валюты введите: /values"
    bot.reply_to(message, text)

@bot.message_handler(commands=["values"])
def currency(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text,key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(" ")
        quote, base, amount = values
        total_base = CurrencyConvector.convert(values)
    except ConvertExcept as e:
        bot.reply_to(message,f"Ошибка пользователя.\n{e}")
    except Exception as e:
        bot.reply_to(message,f"Не удалось обработать команду\n{e}")
    else:
        text= f'Цена {amount} {quote} в {base} - {total_base.get("result")}'
        bot.send_message(message.chat.id, text)


bot.polling()