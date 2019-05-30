import abc
from typing import List

from src.entity.message import Message


class MessengerApi:

    @staticmethod
    @abc.abstractmethod
    def send_msg(chat_id, msg):
        pass

    @staticmethod
    @abc.abstractmethod
    def receive_new() -> List[Message]:
        pass

    @staticmethod
    @abc.abstractmethod
    def receive_all() -> List[Message]:
        pass
