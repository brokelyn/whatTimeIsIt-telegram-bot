from entity.message import Message

from typing import List


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
