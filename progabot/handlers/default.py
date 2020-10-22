from telegram import Update
from telegram.ext import MessageHandler, Filters, CallbackContext


def default(update: Update, context: CallbackContext):
    update.message.reply_dice()


handler = MessageHandler(Filters.all, default)