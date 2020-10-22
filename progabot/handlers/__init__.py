__all__ = ['default']

from importlib import import_module
from pathlib import Path

from telegram.ext import Dispatcher

from progabot.logger import logger


def add_handlers(dispatcher: Dispatcher):
    modules = []
    for f in Path(__file__).parent.glob("*.py"):
        module_name = f.stem
        if not module_name.startswith("_"):
            logger.debug(module_name)
            modules.append(module_name)
            # noinspection PyUnresolvedReferences
            handler = import_module("." + module_name, __package__).handler
            dispatcher.add_handler(handler)
    logger.info("Loaded %s modules. %s", len(modules), modules)
