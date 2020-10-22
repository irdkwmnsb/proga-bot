from progabot.bot import updater
from progabot.logger import logger

logger.debug("Starting polling")
updater.start_polling()
updater.idle()