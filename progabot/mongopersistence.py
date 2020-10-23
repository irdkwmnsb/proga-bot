from telegram.ext import BasePersistence
from pymongo import MongoClient
from pymongo.database import Database
from collections import defaultdict

from progabot.logger import logger


class MongoPersistence(BasePersistence):
    def __init__(self, uri, database,
                 store_user_data=True,
                 store_chat_data=True,
                 store_bot_data=True):
        super().__init__(store_user_data=store_user_data,
                         store_chat_data=store_chat_data,
                         store_bot_data=store_bot_data)
        self.client = MongoClient(uri)
        self.db = self.client[database]  # type: Database
        logger.debug("Connected to %s, %r", uri, self.db)

    def get_user_data(self):
        data = defaultdict(dict)
        for item in self.db["user_data"].find():
            data[item["user_id"]] = item["data"]
        return data

    def get_chat_data(self):
        data = defaultdict(dict)
        for item in self.db["chat_data"].find():
            data[item["chat_id"]] = item["data"]
        return data

    def get_bot_data(self):
        data = {}
        for item in self.db["bot_data"].find():
            data[item["key"]] = item["value"]
        return data

    def get_conversations(self, name):
        data = {}
        for item in self.db[f"conversation.{name}"].find():
            data[tuple(item["conv"])] = item["state"]
        return data

    def update_conversation(self, name, key, new_state):
        self.db[f"conversation.{name}"].update_one({"conv": key}, {"$set": {"state": new_state}}, upsert=True)

    def update_user_data(self, user_id, data):
        self.db["user_data"].update_one({"user_id": user_id}, {"$set": {"data": data}}, upsert=True)

    def update_chat_data(self, chat_id, data):
        self.db["chat_data"].update_one({"chat_id": chat_id}, {"$set": {"data": data}}, upsert=True)

    def update_bot_data(self, data):
        for key, value in data.items():
            self.db["bot_data"].update_one({"key": key}, {"$set": {"value": value}}, upsert=True)
