import operator
import shlex

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from progabot.consts import PREPS
from progabot.logger import logger
from progabot.prep_queue import enqueue_prep, get_position, get_queue


def enter(update: Update, context: CallbackContext):
    lines = ["=!= Очереди =!="]
    for prep, name in PREPS:
        lines.append(f"{name} - {prep}")
        lines.append("".join(get_queue(update, context, prep)))
        lines.append("")
    update.message.reply_text("\n".join(lines))
    return True


handler = CommandHandler(['status', 's'], enter)
