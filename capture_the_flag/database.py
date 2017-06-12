import sqlite3  # noqa

from peewee import SqliteDatabase
from typing import Dict, List, Sequence, Union  # noqa


# HACK: an unencrypted database on the local filesystem is not a good approach
DB_NAME = 'database.db'
sqlite3.connect(DB_NAME)
database = SqliteDatabase('{}'.format(DB_NAME))


def execute(sql, params=None):
    # type: (str, Union[Dict, Sequence]) -> sqlite3.Cursor
    connection = database.get_conn()
    cursor = connection.cursor()
    cursor.execute(sql, params or ())
    connection.commit()
    return cursor


def fetch_all(sql, params=None):
    # type: (str, Union[Dict, Sequence]) -> List[List[Union[str, int, float]]]
    return execute(sql, params).fetchall()


def fetch_row(sql, params=None):
    # type: (str, Union[Dict, Sequence]) -> List[Union[str, int, float]]
    return execute(sql, params).fetchone()


def fetch_value(sql, params=None):
    # type: (str, Union[Dict, Sequence]) -> Union[str, int, float]
    row = fetch_row(sql, params=params)
    return row[0] if row else None


def connect():
    # type: () -> None
    """
    Opens a new database connection if not exists.
    """
    database.connect()


def close(error):
    # type: (Exception) -> None
    """
    Closes the database connection.
    """
    if not database.is_closed():
        database.close()
