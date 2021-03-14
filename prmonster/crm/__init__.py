import sqlite3
from os.path import exists
from .models import CREATE_SQL
from .models import *

DB_FILE = 'data/leads.db'


def get_type(o):
    if isinstance(o, type):
        return o
    else:
        return o.__class__


def table_from(o):
    return get_type(o).__name__.lower() + 's'


def fields_from(o):
    fields = ''
    for field in vars(o).keys():
        if isinstance(field, int):
            fields += f', {field}'
        else:
            fields += f', "{field}"'

    return fields[2:]


def values_from(o):
    fields = ''
    for field in vars(o).values():
        if isinstance(field, int):
            fields += f', {field}'
        else:
            fields += f', "{field}"'

    return fields[2:]


class Connection:
    def __init__(self, db=DB_FILE):
        should_create_tables = not exists(db)
        self.conn = sqlite3.connect(db)
        if should_create_tables:
            for q in CREATE_SQL:
                self.conn.execute(q)
            self.conn.commit()

    def insert(self, o):
        # use upsert
        query = f"""
        INSERT INTO {table_from(o)}
        ({fields_from(o)}) 
        VALUES ({values_from(o)})"""

        """
        ON CONFLICT({o.unique}) 
        DO UPDATE SET
            {field_update_from(o)}
        --WHERE excluded.validDate>phonebook2.validDate;
        """
        self.conn.execute(query)
        self.conn.commit()

        return True

    def select(self, o, **params):
        query = f"""SELECT * FROM {table_from(o)}"""
        results = self.conn.execute(query)
        for result in results:
            yield get_type(o)(*result)


CONN = Connection()


def save_report(report):
    CONN.insert(Repo(
        name=repo.name,
        owner=repo.owner
    ))