# TOKEN: 1183378895:AAFoJKGUoXOAX4dp1oPWws3h6Wl6DM08rTA
# BOT LINK: t.me/crona_karen_bot..

import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, Filters, MessageHandler
from time import sleep
import logging
from telegram import update
from database_man import Database, User
from telegram.ext.dispatcher import run_async

hospital_name = 'Hospital Clinic'
bot_name = 'Karen'
token = '1183378895:AAFoJKGUoXOAX4dp1oPWws3h6Wl6DM08rTA'

updater = Updater(token=token, use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

@run_async
def start(update, context):
    yn_keyboard = [[telegram.InlineKeyboardButton("Yes", callback_data='y1'),
                    telegram.InlineKeyboardButton("No", callback_data='n1')]]

    reply_markup = telegram.InlineKeyboardMarkup(yn_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm {}, a bot designed to get some nice messages across to COVID-19 patients at {}. \n\nWould you like to send a nice message to a random patient?".format(bot_name, hospital_name), reply_markup=reply_markup)

@run_async
def get_name(update, context):
    global name
    name = update.message.text
    dispatcher.remove_handler(plain_text_handler)

    yn_keyboard = [[telegram.InlineKeyboardButton("Yes", callback_data='y2'),
                    telegram.InlineKeyboardButton("No", callback_data='n2')]]

    reply_markup = telegram.InlineKeyboardMarkup(yn_keyboard)
    name_text = "Nice to meet you <b>{}</b>! I'm excited to get your message to one of our patients!\nDid I get your name right?".format(name)
    query.edit_message_text(parse_mode='HTML', text=name_text, reply_markup=reply_markup)

@run_async
def get_name_again(update, context):
    global name
    name = update.message.text
    dispatcher.remove_handler(plain_text_handler)

    yn_keyboard = [[telegram.InlineKeyboardButton("Yes", callback_data='y2'),
                    telegram.InlineKeyboardButton("No", callback_data='n2')]]

    reply_markup = telegram.InlineKeyboardMarkup(yn_keyboard)
    name_text = "Got it <b>{}</b>! I'm really happy to get your message to one of our patients!\nDid I get your name right?".format(name)
    query.edit_message_text(parse_mode='HTML', text=name_text, reply_markup=reply_markup)

@run_async
def ask_if_message_ready(update, context):
    yn_keyboard = [[telegram.InlineKeyboardButton("Ready", callback_data='y3')]]
    reply_markup = telegram.InlineKeyboardMarkup(yn_keyboard)
    query.edit_message_text(text='Cool! Do you have the message you want to send ready?\nHere are some of the guidelines it should follow:\n- Be positive.\n- Keep it under 3000 characters.\n- Avoid talking about the virus.', reply_markup=reply_markup)

@run_async
def message_too_long(update, context):
    yn_keyboard = [[telegram.InlineKeyboardButton("Ready", callback_data='y3')]]
    reply_markup = telegram.InlineKeyboardMarkup(yn_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm sorry {}, your message is over 3000 characters and can't be sent. Please make it shorter and send it again".format(name), reply_markup=reply_markup)

@run_async
def get_message(update, context):
    global message
    message = update.message.text
    dispatcher.remove_handler(plain_text_handler)
    if len(message) > 3000:
        message_too_long(update, context)
    yn_keyboard = [[telegram.InlineKeyboardButton("Send it!", callback_data='y4'),
                    telegram.InlineKeyboardButton("Let me rewrite...", callback_data='n4')]]
    reply_markup = telegram.InlineKeyboardMarkup(yn_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Beautiful message {}! I'm sure your it will be appreciated.\nReady to send it or would you like to rewrite something?".format(name), reply_markup=reply_markup)

@run_async
def get_message_rewrite(update, context):
    global message
    message = update.message.text
    dispatcher.remove_handler(plain_text_handler)
    if len(message) > 3000:
        message_too_long(update, context)
    yn_keyboard = [[telegram.InlineKeyboardButton("Send it!", callback_data='y4'),
                    telegram.InlineKeyboardButton("Let me rewrite...", callback_data='n4')]]
    reply_markup = telegram.InlineKeyboardMarkup(yn_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Nice changes to your message {}! I'm sure your it will make someone feel great.\nReady to send it or would you like to rewrite something?".format(name), reply_markup=reply_markup)

@run_async
def button(update, context):
    global plain_text_handler
    global query
    query = update.callback_query
    query.answer()

    if query.data == 'y1':
        query.edit_message_text(text="Awesome! Thank you for taking the time to say something nice :)\nWhat should I call you?\n\n(Please type in your name below)")
        plain_text_handler = MessageHandler(Filters.text, get_name)
        dispatcher.add_handler(plain_text_handler)
    if query.data == 'n1':
        query.edit_message_text(text="Alright, well, send me a message saying '/start' whenwver you feel ready to send one.")

    if query.data == 'y2':
        ask_if_message_ready(update, context)        
    if query.data == 'n2':
        query.edit_message_text(text="Oh, sorry, please send me your name again.")
        plain_text_handler = MessageHandler(Filters.text, get_name_again)
        dispatcher.add_handler(plain_text_handler)

    if query.data == 'y3':
        query.edit_message_text(text="Neat! Please send your message now.")
        plain_text_handler = MessageHandler(Filters.text, get_message)
        dispatcher.add_handler(plain_text_handler)

    if query.data == 'y4':
        query.edit_message_text(text="Yay! Your message was sent successfully!\nThank you for making someone's day better :)\nI hope to see you soon <3")
        context.bot.send_photo(chat_id=update.effective_chat.id, photo='https://66.media.tumblr.com/c07d5a8b7b6d8a16fda81852307b7828/tumblr_inline_os2hl4YXrK1sp11ym_540.png')
        chat_id = update.effective_chat.id
        db = Database('database.csv')
        new_user = User(chat_id, name, message)
        db.store_user(new_user)
    if query.data == 'n4':
        query.edit_message_text(text="Please send your rewritten message now.")
        plain_text_handler = MessageHandler(Filters.text, get_message_rewrite)
        dispatcher.add_handler(plain_text_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

yesno_handler = CallbackQueryHandler(button)
dispatcher.add_handler(yesno_handler)

updater.start_polling()