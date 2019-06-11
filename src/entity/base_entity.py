import peewee, os
import urllib.parse


def connect_db():
    if 'HEROKU' not in os.environ:
        db = peewee.SqliteDatabase('WhatTimeIsIt.db')
    else:
        urllib.parse.uses_netloc.append('postgres')
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])
        db = peewee.PostgresqlDatabase(database=url.path[1:], user=url.username,
                                       password=url.password, host=url.hostname,
                                       port=url.port, sslmode="require")
    return db


class BaseEntity(peewee.Model):
    class Meta:
        database = connect_db()
