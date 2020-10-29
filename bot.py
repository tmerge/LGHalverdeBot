import datetime
import yaml
import util

from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, Bot, ForceReply
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler

#load config
with open('config.yaml', 'r') as f:
    cfg = yaml.load(f, Loader=yaml.FullLoader)


STRECKE, MELDER, CHOOSING, CONCLUSION = range(4)

# handle all messages 
def messageHandler(update, context): 
    reply_markup = ReplyKeyboardMarkup([['Melder 📟', 'Strecke🧯⏱', 'Abbrechen']], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(f'Hallo {update.effective_user.first_name}, wie kann ich dir helfen?', reply_markup=reply_markup)
    return CHOOSING

# handle melder related stuff
def melderHandler(update, context):
    context.user_data['meldung'] = update.message.text
    reply_markup = ReplyKeyboardMarkup([['Nicht ausgelöst', 'Defekt', 'Abbrechen']], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text('Was genau möchtest du melden?', reply_markup = reply_markup)
    return MELDER

def streckenHandler(update, context):
    update.message.reply_text(f'Strecken Termine für {datetime.date.today().year + 1}:\n11.02.2021 (Termin 1)\n08.06.2021 (Termin 2)\n24.08.2021 (Termin 3)')    
    return ConversationHandler.END


def melderDefektHandler(update, context):
    reply_markup = ReplyKeyboardMarkup([['Ja', 'Nein', 'Abbrechen']], resize_keyboard=True, one_time_keyboard=True)
    update.message.reply_text(f'Dein Melder ist also defekt?', reply_markup=reply_markup)
    return CONCLUSION

def melderRequestHandler(update, context): 
    update.message.reply_text(f'Wo lag der Melder?')
    return CONCLUSION

def abbrechen(update, context):
    update.message.reply_text('Wenn ich dir mal wieder helfen soll, melde dich!', reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()

# main part of bot
def main():

    updater = Updater(cfg['token'], use_context=True)
    dp = updater.dispatcher
    
    #conversation handler
    conversationHandler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(r'[a-zA-Z0-9]*'), messageHandler)],
    states={
        CHOOSING: [ 
            MessageHandler(Filters.regex(r'^Melder'), melderHandler),
            MessageHandler(Filters.regex(r'^Strecke'), streckenHandler),
            MessageHandler(Filters.regex(r'^Abbrechen$'), abbrechen)
        ],

        MELDER: [
            MessageHandler(Filters.regex(r'^Nicht ausgelöst'), melderRequestHandler),
            MessageHandler(Filters.regex(r'^Defekt'), melderDefektHandler),
            MessageHandler(Filters.regex(r'^Abbrechen$'), abbrechen)
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