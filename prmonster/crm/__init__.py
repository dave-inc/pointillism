import logging
import sqlite3
from os.path import exists
from .models import *
from .models import Repo, Resource

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
        elif field is None:
            fields += ", NULL"
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

    def execute(self, query):
        self.conn.execute(query)
        self.conn.commit()
        return True

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
        cursor = self.conn.cursor()
        cursor.execute(query)
        id_ = cursor.lastrowid
        self.conn.commit()
        return id_

    def select(self, o=None, query=None, cast=False, **params):
        if query is None:
            cast = True
            query = f"""SELECT * FROM {table_from(o)}"""
        results = self.conn.execute(query)

        for result in results:
            if cast:
                yield get_type(o)(*result)
            else:
                yield result

CONN = Connection()


def save_report(report):
    try:
        repo_id = CONN.insert(report.repo)
    except sqlite3.IntegrityError:
        logging.info(f"Repo exists: {report.repo}")
        return

    for res in report.dots: # + report.dot_refs:
        CONN.insert(Resource(
            repo_id=repo_id,
            filename=str(res)
        ))

def all_repos():
    return CONN.select(Repo)

def all_resources():
    return CONN.select(Resource)

def repo_count():
    return next(CONN.select(query=REPO_COUNT))[0]

def repos_over_days():
    return [row for row
            in CONN.select(query=REPOS_OVER_DAYS)]
