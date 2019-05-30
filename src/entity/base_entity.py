import peewee

db = peewee.SqliteDatabase('WhatTimeIsIt.db')


class BaseEntity(peewee.Model):
    class Meta:
        database = db
