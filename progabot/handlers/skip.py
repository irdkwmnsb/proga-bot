import operator
import shlex

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters

from progabot.consts import PREPS, ADMINS
from progabot.logger import logger
from progabot.prep_queue import enqueue_prep, pop_prep, alert_next


def skip(update: Update, context: CallbackContext):
    args = shlex.split(update.message.text.lower())
    if len(args) != 2:
        update.message.reply_text("Forgot prep")
    else:
        prep = args[1]
        if prep in map(operator.itemgetter(0), PREPS):
            try:
                task_n, next_user, username = pop_prep(update, context, prep)
                update.message.reply_text(
                    f"Skipped {context.dispatcher.bot_data.get(prep, 'nobody')}. Next is @{username} for task {task_n}")
                context.bot_data[prep + "_at"] = next_user
                context.dispatcher.user_data[next_user]["last_at"] = prep
                context.bot.send_message(next_user, f"Ваша очередь!\n"
                                                    f"Вы сдаёте задачу {task_n} преподавателю <b>{prep}</b>.\n"
                                                    f"Пожалуйста не задерживайте очередь и как только уйдёте от препода"
                                                    f" - напишите /done.", parse_mode="HTML")
                alert_next(update, context, prep)
            except IndexError as e:
                update.message.reply_text("Queue is empty.")
            return True
        update.message.reply_text("No such prep")


handler = CommandHandler(["skip"], skip, filters=Filters.user(ADMINS))
