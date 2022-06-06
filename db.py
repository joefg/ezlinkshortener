import os
import sqlite3

SQL_LOCATION = 'sql/'

def connect(location):
    def factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0].lower()] = row[idx]
        return d

    conn = sqlite3.connect(os.path.join(location))
    conn.row_factory = factory
    cur = conn.cursor()

    return conn, cur

def create(location):
    conn, cur = connect(os.path.join(location))

    with open(os.path.join(SQL_LOCATION, 'base.sql'), 'r') as base:
        cur.executescript(base.read())

    conn.commit()
    conn.close()
