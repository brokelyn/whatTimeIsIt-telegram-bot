from entity.message import Message
from entity.statistic import Statistic

from typing import List


class MessageRepo:

    @staticmethod
    def create(msg: Message):
        msg.save(force_insert=True)

    @staticmethod
    def save(msg: Message):
        msg.save()

    @staticmethod
    def findAll() -> List[Message]:
        return list(Message.select())

    @staticmethod
    def findByStatistic(stat: Statistic) -> List[Message]:
        return list(Message.select().where(Message.id > stat.last_msg_id,
                                           Message.group == stat.group))

    @staticmethod
    def sameTimeSameUserMessageExists(msg) -> bool:
        msg_dt_start = msg.date.replace(second=0)
        msg_dt_end = msg.date.replace(second=59)
        query = Message.select().where(Message.time >= msg_dt_start,
                                       Message.time <= msg_dt_end,
                                       Message.user == msg.from_user.id)
        return query.exists()
