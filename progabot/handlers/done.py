import operator
import shlex

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from progabot.consts import PREPS
from progabot.logger import logger
from progabot.prep_queue import enqueue_prep, pop_prep, alert_next


def done(update: Update, context: CallbackContext):
    prep = context.user_data.get("last_at", None)
    if prep is None or context.dispatcher.bot_data.get(prep+"_at", None) != update.effective_user.id:
        update.message.reply_text("Сейчас не ваша очередь.")
        return
    try:
        task_n, next_user, username = pop_prep(update, context, prep)
        context.user_data["last_at"] = None
        update.message.reply_text("Спасибо! Вы вышли из очереди. Если вы были записаны в другие очереди - не "
                                  f"забудьте заново записаться")
        context.dispatcher.user_data[next_user]["last_at"] = prep
        context.bot_data[prep+"_at"] = next_user
        context.bot.send_message(next_user, f"Ваша очередь!\n"
                                            f"Вы сдаёте задачу {task_n} преподавателю <b>{prep}</b>.\n"
                                            f"Пожалуйста не задерживайте очередь и как только уйдёте от препода -"
                                            f" напишите /done", parse_mode="HTML")
        alert_next(update, context, prep)
    except IndexError as e:
        update.message.reply_text("Похоже что за вами в очереди никого нет (чудеса). "
                                  "Простите, но я не умею работать когда у преподавателя никто не сидит. "
                                  "Поэтому посидите у него ещё и напишите /done через некоторое время.))\n"
                                  "Или как вариант можете записаться к этому преподавателю ещё раз "
                                  "и написать /done чтобы накрутить себе подходы))))")



handler = CommandHandler(['done'], done)
