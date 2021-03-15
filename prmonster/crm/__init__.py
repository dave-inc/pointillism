import sqlite3
from os.path import exists
from .models import CREATE_SQL
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
            yield result


CONN = Connection()


def save_report(report):
    name, owner = report.repo.split("/") # TODO drop this line
    repo_id = CONN.insert(Repo(
        name=name,
        owner=owner
    ))
    for res in report.dots: # + report.dot_refs:
        CONN.insert(Resource(
            repo_id=repo_id,
            filename=str(res)
        ))

def all_repos():
    return CONN.select(Repo)

def all_resources():
    return CONN.select(Resource)