# TOKEN: 1131987867:AAHJaISmTFrGqJ5Z1al80VY94Zim0gJVYiA

import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from time import sleep

import logging
from telegram import update

hospital_name = 'Hospital Clinic'

updater = Updater(token='1131987867:AAHJaISmTFrGqJ5Z1al80VY94Zim0gJVYiA', use_context=True)

dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def start(update, context):
    
    keyboard = [[telegram.InlineKeyboardButton("Yes", callback_data='y'),
                 telegram.InlineKeyboardButton("No", callback_data='n')]]

    reply_markup = telegram.InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm Coronita, a bot designed to get some nice messages across to COVID-19 patients at {}. \n\nWould you like to send a nice message to a random patient?".format(hospital_name), reply_markup=reply_markup)

def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    if query.data == 'y':
        context.bot.send_message(chat_id=update.effective_chat.id, text="Awesome! Now I'm gonna ask you some simple questions, are you ready?".format(hospital_name), reply_markup=reply_markup)
    elif query.data == 'n':
        print('Selcted no.')


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

yesno_handeler = CallbackQueryHandler(button)
dispatcher.add_handler(yesno_handeler)

updater.start_polling()