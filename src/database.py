import peewee

from src.entity.message import Message
from src.entity.user import User
from src.entity.score import Score
from src.entity.statistic import Statistic


def init():
    db = peewee.SqliteDatabase('WhatTimeIsIt.db')

    db.create_tables([User, Message, Score, Statistic])
