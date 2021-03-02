import sqlite3
from os.path import exists
from .models import CREATE_SQL

DB_FILE = 'data/leads.db'


def table_from(o):
    if isinstance(o, type):
        return o.__name__.lower() + 's'
    else:
        return o.__class__.__name__.lower() + 's'


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
        query = f"""
        INSERT INTO {table_from(o)}
        ({fields_from(o)}) 
        VALUES ({values_from(o)})"""
        self.conn.execute(query)
        self.conn.commit()

        return True

    def select(self, o, **params):
        query = f"""SELECT * FROM {table_from(o)}"""
        return self.conn.execute(query)
