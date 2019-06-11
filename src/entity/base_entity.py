import peewee

import database as db_conn


class BaseEntity(peewee.Model):
    class Meta:
        database = db_conn.connect_db()
