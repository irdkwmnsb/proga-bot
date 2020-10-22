import logging
import datetime
from pathvalidate import sanitize_filename
logger = logging.root
logger.setLevel(logging.DEBUG)

log_formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)-5.5s] --- %(message)s")

fname = sanitize_filename(datetime.datetime.now().strftime("log_%x_%X%p.log"))
file_handler = logging.FileHandler(f"./logs/{fname}", encoding="UTF-8")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(log_formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.DEBUG)
logger.addHandler(console_handler)