import telebot 
import random

TOKEN = "7139285452:AAHolhbKYBREl7gDTjR9r34v58amU4ysJPs"
bot = telebot.TeleBot(TOKEN)

UPLOAD_FOLDER = r"C:\memes/"

memes = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg", "6.jpg", "7.jpg", "8.jpg", "9.jpg", "10.jpg",
          "11.jpg", "12.jpg", "13.jpg", "14.jpg", "15.jpg", "16.jpg", "17.jpg", "18.jpg", "19.jpg", "20.jpg",]

reactions = ["Very funny(sarcastic tone)", "AHAHAHAHA, okay, you got me", "Wow, that was original"]

@bot.message_handler(content_types=["photo"])
def receive_meme(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    file_name = str(len(memes) + 1) + ".jpg"
    with open(UPLOAD_FOLDER + file_name, "wb") as new_file:
        new_file.write(downloaded_file)
    memes.append(file_name)
    bot.reply_to(message, "Got the meme!")

@bot.message_handler(commands=["meme"])
def send_random_meme(message):
    if memes:
        meme = random.choice(memes)
        with open(UPLOAD_FOLDER + meme, "rb") as photo:
            sent_message = bot.send_photo(message.chat.id, photo)
            bot.send_message(
                message.chat.id,
                "Did you like it? Answer:: 👍 or 👎",
                reply_to_message_id=sent_message.message_id
            )
    else:
        bot.reply_to(message, "Theres no memes at the moment :(")

@bot.message_handler(func=lambda message: message.text in ["👍", "👎"])
def handle_reaction(message):
    if message.text == "👍":
        bot.reply_to(message, "Glad you liked it 😊")
    elif message.text == "👎":
        bot.reply_to(message, "It's a pity 😢, I'll try to find something more interesting next time!")

@bot.message_handler(commands=["start"])
def welcome(message):
    bot.send_message(message.chat.id, "Hi, here we have memes. Type [meme] and I will show you some")

@bot.message_handler(commands=["count"])
def meme_count(message):
    if memes:
        memes_count = len(memes)
        bot.reply_to(message, f"Added {memes_count} memes")
    else:
        bot.reply_to(message, "Theres no memes at the moment :(")

bot.polling()