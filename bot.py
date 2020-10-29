import datetime
import yaml

from telegram import Update, ReplyKeyboardMarkup, Bot, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler

#load config
with open('config.yaml', 'r') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)


STRECKE, MELDER, CHOOSING = range(3)

# handle all messages 
def messageHandler(update, context): 
    reply_markup = ReplyKeyboardMarkup([['Melder', 'Strecke']], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(f'Hallo {update.effective_user.first_name}, wie kann ich dir helfen?', reply_markup=reply_markup)
    return CHOOSING

# handle melder related stuff
def melderHandler(update, context):
    reply_markup = ReplyKeyboardMarkup([['Nicht ausgelöst', 'Defekt']], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Was genau möchtest du melden?', reply_markup = reply_markup)
    return ConversationHandler.END

def streckenHandler(update, context):
    update.message.reply_text(f'Strecken Termine für {datetime.date.today().year + 1}:\n 11.02.2021 (Termin 1)\n 08.06.2021 (Termin 2)\n 24.08.2021 (Termin 3)')    
    return ConversationHandler.END

def abbrechen():
    pass

# main part of bot
def main():

    updater = Updater(cfg['token'], use_context=True)
    dp = updater.dispatcher
    
    #conversation handler
    conversationHandler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(r'[a-zA-Z0-9]*'), messageHandler)],
    states={
        CHOOSING: [ 
            MessageHandler(Filters.regex(r'[Melder]'), melderHandler),
            MessageHandler(Filters.regex(r'[Strecke]'), streckenHandler)
        ]
    },
    fallbacks=[CommandHandler('abbrechen', abbrechen)])
    
    # bind conversation handler 
    dp.add_handler(conversationHandler)
    
    # start bot 
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()