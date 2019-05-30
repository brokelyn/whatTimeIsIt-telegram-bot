from src.entity.message import Message
from src.messenger.telegram.telegram_api import TelegramApi


class EventController:

    @staticmethod
    def create_event(msg: Message):
        TelegramApi.send_msg(msg.chat_id, "'/createEvent' is currently not supported")

    @staticmethod
    def remove_event(msg: Message):
        TelegramApi.send_msg(msg.chat_id, "'/removeEvent' is currently not supported")
