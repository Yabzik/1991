import telebot
import config

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=["start"])
def start_msg(message):
    bot.send_message(message.chat.id, "Стартуем!")

@bot.message_handler(commands=["help"])
def help_msg(message):
    bot.send_message(message.chat.id, "Ничем помочь не могу(")

if __name__ == "__main__":
    bot.polling(none_stop=True)
