import peewee

import database as db


class BaseEntity(peewee.Model):
    class Meta:
        database = db.connection
