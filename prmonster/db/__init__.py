import sqlite3

class Connection:
    def __init__(self, dbname='.leads.db'):
        self.conn = sqlite3.connect(dbname)

    def execute(self, sql, *params):
        """
        TODO needs commiting if insert
        :param sql:
        :param params:
        :return:
        """
        c = self.conn.cursor()
        return c.execute(sql, *params)

    def insert(self, table, **params):
        c = self.conn.cursor()
        c.execute(f"""
        INSERT INTO {table}
        ({params.keys()})
        VALUES ({params.values()});
        """)

