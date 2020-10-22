import telegram.ext
from telegram.utils.request import Request

from progabot.consts import TOKEN

from progabot.utils import MQBot
from progabot.handlers import add_handlers

request = Request(con_pool_size=8)
testbot = MQBot(TOKEN, request=request)
updater = telegram.ext.updater.Updater(bot=testbot, use_context=True)
add_handlers(updater.dispatcher)