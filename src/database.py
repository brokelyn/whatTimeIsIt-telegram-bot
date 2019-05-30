import peewee

from src.entity.bot import Bot
from src.entity.event import Event
from src.entity.message import Message
from src.entity.score import Score
from src.entity.user import User


def init():
    db = peewee.SqliteDatabase('WhatTimeIsIt.db')

    db.create_tables([Event, User, Message, Score, Bot])

    Bot(name="1337").save()

    print("DB ready!")
