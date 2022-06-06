import os
import argparse
import logging

import sqlite3

SQL_LOCATION = 'sql/'

def connect(location):
    def factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0].lower()] = row[idx]
        return d

    if os.path.exists(os.path.join(location)):
        conn = sqlite3.connect(os.path.join(location))
        conn.row_factory = factory
        cur = conn.cursor()
    else:
        raise Exception("Database does not exist. No connection created.")

    return conn, cur

def create(location):
    if os.path.exists(os.path.join(location)):
        raise Exception("Database already exists. Aborting.")

    open(os.path.join(location), 'a').close()

    conn, cur = connect(os.path.join(location))

    with open(os.path.join(SQL_LOCATION, 'base.sql'), 'r') as base:
        cur.executescript(base.read())

    conn.commit()
    conn.close()

def update(location):
    raise NotImplementedError("Not implemented yet.")
    conn, cur = connect(os.path.join(location))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Database Manager'
    )

    parser.add_argument(
        'path',
        nargs=1,
        help='Location of data store'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Increase output verbosity'
    )

    parser.add_argument(
        '--create', '-c',
        action='store_true',
        help='Create new database'
    )

    parser.add_argument(
        '--update', '-u',
        action='store_true',
        help='Update existing database'
    )

    args = vars(parser.parse_args())

    if args['verbose']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARN)

    logging.debug("Arguments:" + str(args))

    path = args['path'][0]

    if args['create']:
        create(os.path.join(path))
        logging.info(f"Created new database at {path}")

    if args['update']:
        update(os.path.join(path))
