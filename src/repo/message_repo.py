from src.entity.message import Message


class MessageRepo:

    @staticmethod
    def save(msg: Message):
        msg.save()

    @staticmethod
    def findAll():
        return list(Message.select())
