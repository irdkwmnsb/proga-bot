__all__ = ['default', 'add_handlers']

from importlib import import_module
from pathlib import Path

from telegram.ext import Dispatcher

from progabot.logger import logger

module_names = ["enter", "leave", "done", "skip", "populate", "default", "status"]


def add_handlers(dispatcher: Dispatcher):
    for module_name in module_names:
        module = import_module("." + module_name, __package__)
        logger.debug(module_name)
        # noinspection PyUnresolvedReferences
        assert hasattr(module, "handler")
        handler = module.handler
        dispatcher.add_handler(handler)
    logger.info("Loaded %s modules. %s", len(module_names), module_names)
