import peewee, os


def connect_db():
    if os.environ['ENV'] == 'dev':
        db = peewee.SqliteDatabase('WhatTimeIsIt.db')
    else:
        db = peewee.PostgresqlDatabase(os.environ['DATABASE_URL'])
    return db


class BaseEntity(peewee.Model):
    class Meta:
        database = connect_db()
