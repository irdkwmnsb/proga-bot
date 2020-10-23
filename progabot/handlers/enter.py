import operator
import shlex

from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

from progabot.consts import PREPS
from progabot.logger import logger
from progabot.prep_queue import enqueue_prep, get_position


def enter(update: Update, context: CallbackContext):
    logger.debug("enqueue")
    args = shlex.split(update.message.text.lower())
    lines = []
    if len(args) <= 2:
        lines.append(f"Пожалуйста укажите преподавателя и номер задачи")
    elif len(args) > 2:
        prep_name = args[1]
        task_n = args[2]
        if not task_n.isdigit():
            lines.append(f"Номер задачи должен быть числом")
        elif prep_name in map(operator.itemgetter(0), PREPS):
            if enqueue_prep(update, context, prep_name, int(task_n)):
                update.message.reply_text(
                    f"Успешно записали. Перед вами {get_position(update, context, prep_name, update.effective_user.id)} человек.")
            return True
    lines.append(f"Сейчас можно записаться к {len(PREPS)} преподавателям")
    for initials, name in PREPS:
        lines.append(f"{name}: /e {initials} [номер задачи]")
    update.message.reply_text("\n".join(lines))


handler = CommandHandler(['enqueue', 'e'], enter)
