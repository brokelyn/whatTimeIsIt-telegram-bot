from entity.message import Message

from typing import List
from datetime import datetime


class MessageRepo:

    @staticmethod
    def create(msg: Message):
        msg.save(force_insert=True)

    @staticmethod
    def save(msg: Message):
        msg.save()

    @staticmethod
    def findAll():
        return list(Message.select())

    @staticmethod
    def findByIdIsGreater(id: int) -> List[Message]:
        return list(Message.select().where(Message.id > id))

    @staticmethod
    def sameTimeSameUserMessageExists(msg) -> bool:
        msg_dt_start = msg.date.replace(second=0)
        msg_dt_end = msg.date.replace(second=59)
        query = Message.select().where(Message.time >= msg_dt_start,
                                       Message.time <= msg_dt_end,
                                       Message.user == msg.from_user.id)
        return query.exists()
