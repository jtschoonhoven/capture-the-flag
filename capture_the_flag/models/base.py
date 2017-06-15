from datetime import datetime
from peewee import DateTimeField, Model
from capture_the_flag import database as db


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.utcnow)

    class Meta(object):
        database = db.database
