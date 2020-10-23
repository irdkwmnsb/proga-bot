import random

from telegram import Update
from telegram.ext import CallbackContext

from progabot.consts import PREPS


def enqueue_prep(update: Update, context: CallbackContext, prep, task_number):
    user = update.effective_user.id
    for i, (_, _, _, _, id, username) in enumerate(context.bot_data[prep]):
        if id == user:
            update.message.reply_text(f"Вы уже записаны к {prep}. Ваше место в очереди - {i}")
            return False
    else:
        if not "rand" in context.user_data:
            context.user_data["rand"] = random.randint(0, 100000)
        context.bot_data[prep].append([
            context.user_data.get("visits", 0),
            context.user_data.get(f"visits_{prep}", 0),
            task_number,
            context.user_data.get("rand"),
            user,
            update.effective_user.username
        ])
        context.bot_data[prep].sort()
    return True


def pop_prep(update: Update, context: CallbackContext, prep):
    if not context.bot_data[prep]:
        raise IndexError()
    visits, visits_prep, task_n, rand, user, username = context.bot_data[prep][0]
    if user:
        context.dispatcher.user_data[user]["visits"] = visits + 1
        context.dispatcher.user_data[user][f"visits_{prep}"] = visits_prep + 1
        context.bot_data[prep].pop(0)
        for prep, name in PREPS:
            dequeue_prep(update, context, prep, user)
    return task_n, user, username


def dequeue_prep(update: Update, context: CallbackContext, prep, user):
    for i, (_, _, _, _, id, username) in enumerate(context.bot_data[prep]):
        if id == user:
            context.bot_data[prep].pop(i)
            context.bot_data[prep].sort()
            break


def get_position(update: Update, context: CallbackContext, prep, user):
    for i, (_, _, _, _, id, username) in enumerate(context.bot_data[prep]):
        if id == user:
            return i


def alert_next(update: Update, context: CallbackContext, prep):
    for i, (_, _, _, _, id, username) in enumerate(context.bot_data[prep]):
        context.bot.send_message(id, f"В очереди к {prep} перед вами {i} человек.\n"
                                     f"Пожалуйста будьте готовы подойти к преподавателю, когда настанет ваша очередь")


def get_queue(update: Update, context: CallbackContext, prep):
    return [f"@{i[5]}" for i in context.bot_data[prep]]