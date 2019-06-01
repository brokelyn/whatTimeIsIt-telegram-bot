from src.entity.message import Message


class MessageRepo:

    @staticmethod
    def save(msg: Message):
        msg.save(force_insert=True)

    @staticmethod
    def findAll():
        return list(Message.select())
