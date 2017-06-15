import random
import time
import os

os.chdir('<desired-directory>')

from peewee import DoesNotExist, PrimaryKeyField, TextField
from flask_login.mixins import UserMixin
from capture_the_flag import database as db
from capture_the_flag.models.base import BaseModel


def generate_uid():
    """
    Generate a pseudorandom 64-bit number.
    The first part of the number is the current time in epoch ms.

    Not a hack. This is sure to be unique (in practice) and sorts chronologically.
    Could also include a PID, the IP of the host, and auto-incrementing bits.
    """
    global sequence_val
    epoch_ms = int(time.time() * 1000)
    bit_len = epoch_ms.bit_length()

    # shift epoch_ms left to make it a 64-bit integer, then randomize the rest
    uid = epoch_ms << 64 - bit_len
    uid = uid | random.getrandbits(64 - bit_len)

    return unicode(uid)


def load_user_from_session(id):
    try:
        # HACK: should match on session_token, not permanent ID
        user = User.get(User.id == int(id))
    except (DoesNotExist, ValueError, TypeError):
        return None
    return user


class User(BaseModel, UserMixin):
    # HACK: autoincrementing ids are easy to guess
    id = PrimaryKeyField()
    username = TextField(unique=True)
    # HACK: plaintext passwords, lol
    password = TextField()
    file_access_path = TextField(default='shared/public')
    session_token = TextField(unique=True, default=generate_uid)

    def get_id(self):
        # HACK: this should use session_token
        return unicode(self.id)

    class Meta(object):
        db_table = 'users'
