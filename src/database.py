import urllib.parse

import os
import peewee


def connect_db():
    if 'DATABASE_URL' not in os.environ:
        db = peewee.SqliteDatabase('WhatTimeIsIt.db', autorollback=True, autocommit=True)
        print("Local SQLite DB active")
    else:
        urllib.parse.uses_netloc.append('postgres')
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        db = peewee.PostgresqlDatabase(database=url.path[1:], user=url.username,
                                       password=url.password, host=url.hostname,
                                       port=url.port, sslmode="require",
                                       autorollback=True, autocommit=True)
        print("Postgres DB active")
    return db


def init():
    from entity.message import Message
    from entity.user import User
    from entity.statistic import Statistic
    from entity.score import Score
    from entity.event import Event
    from entity.group import Group

    connection.create_tables([User, Message, Group, Statistic, Score, Event])


connection = connect_db()
