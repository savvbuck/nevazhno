import telebot


token = '7204734336:AAGpG5Ovp1-r8btiPDfZsK3fgtdu7C-uj4w'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
bot.infinity_polling()