import peewee

from entity.message import Message
from entity.user import User
from entity.statistic import Statistic
from entity.score import Score

def init():
    db = peewee.SqliteDatabase('WhatTimeIsIt.db')

    db.create_tables([User, Message, Score, Statistic])
