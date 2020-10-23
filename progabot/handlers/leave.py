import operator
import shlex

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from progabot.consts import PREPS
from progabot.logger import logger
from progabot.prep_queue import enqueue_prep, dequeue_prep, alert_next


def leave(update: Update, context: CallbackContext):
    logger.debug("enqueue")
    args = shlex.split(update.message.text.lower())
    if len(args) == 1:
        update.message.reply_text(f"Вы забыли указать преподавателя!")
    elif len(args) >= 1:
        prep_name = args[1]
        update.message.reply_text("Вы вышли из очереди")
        dequeue_prep(update, context, prep_name)
        alert_next(update, context, prep_name)
    return True


handler = CommandHandler(['leave', 'l'], leave)
