from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, Filters, CallbackContext, CommandHandler
from progabot.consts import ADMINS, PREPS

from progabot.logger import logger


def populate(update: Update, context: CallbackContext):
    logger.debug("populate")
    lines = []
    for initials, name in PREPS:
        if initials in context.bot_data and isinstance(context.bot_data[initials], list):
            lines.append(f"{initials} is already initialized and has {len(context.bot_data[initials])} entries")
        else:
            #context.bot_data[initials] = [[-float('inf'), -float('inf'), -float('inf'), -float('inf'), None, ""]]
            context.bot_data[initials] = []
    lines.append(f"done")
    update.message.reply_text("\n".join(lines))
    return True


handler = CommandHandler("populate", populate, filters=Filters.user(ADMINS))
