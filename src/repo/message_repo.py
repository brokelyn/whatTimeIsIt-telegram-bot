from src.entity.message import Message


class MessageRepo:

    @staticmethod
    def save(msg: Message):
        msg.save()
