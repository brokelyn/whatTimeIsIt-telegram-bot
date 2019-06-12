import peewee, os
import urllib.parse


def connect_db():
    if 'HEROKU' not in os.environ:
        db = peewee.SqliteDatabase('WhatTimeIsIt.db')
        print("Local SQLite DB active")
    else:
        urllib.parse.uses_netloc.append('postgres')
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        db = peewee.PostgresqlDatabase(database=url.path[1:], user=url.username,
                                       password=url.password, host=url.hostname,
                                       port=url.port, sslmode="require")
        print("Heroku Postgres DB active")
    return db

def init():
    db = connect_db()

    from entity.message import Message
    from entity.user import User
    from entity.statistic import Statistic
    from entity.score import Score

    db.create_tables([User, Message, Score, Statistic])

    db.close()
