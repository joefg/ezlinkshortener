import os
import sqlite3

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
