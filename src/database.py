import peewee, os

from entity.message import Message
from entity.user import User
from entity.statistic import Statistic
from entity.score import Score


def connect_db():
    if os.environ['ENV'] == 'dev':
        db = peewee.SqliteDatabase('WhatTimeIsIt.db')
    else:
        db = peewee.PostgresqlDatabase(os.environ['DATABASE_URL'])
    return db

def init():
    db = connect_db()

    db.create_tables([User, Message, Score, Statistic])
