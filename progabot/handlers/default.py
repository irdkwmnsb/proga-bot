from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, Filters, CallbackContext

from progabot.logger import logger


def default(update: Update, context: CallbackContext):
    logger.debug("default")
    lines = ["=!= Команды =!="]
    if context.user_data.get("queues_count", 0) == 0:
        lines.append("Встать в очередь /e")
    else:
        lines.append("Выйти из очереди /d")
    lines.append("Статус /s - пока не работает")
    update.message.reply_text("\n".join(lines))
    return True


handler = MessageHandler(Filters.all, default)
