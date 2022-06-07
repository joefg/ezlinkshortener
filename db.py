import os
import argparse
import logging

import sqlite3

SQL_LOCATION = 'sql/'

def connect(location, debug=False):
    def factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0].lower()] = row[idx]
        return d

    def trace_callback(msg):
        logging.debug("Database trace:")
        logging.debug(msg)

    if os.path.exists(os.path.join(location)):
        conn = sqlite3.connect(os.path.join(location))
        conn.row_factory = factory
        cur = conn.cursor()
    else:
        raise Exception("Database does not exist. No connection created.")

    if debug:
        conn.set_trace_callback(trace_callback)

    return conn, cur

def create(location):
    if os.path.exists(os.path.join(location)):
        raise Exception("Database already exists. Aborting.")

    open(os.path.join(location), 'a').close()

    conn, cur = connect(os.path.join(location), debug=True)

    with open(os.path.join(SQL_LOCATION, 'base.sql'), 'r') as base:
        cur.executescript(base.read())

    conn.commit()
    conn.close()

def update(location):
    exclude = ('base.sql')
    files = [f for f in os.listdir(os.path.join('sql')) if f[-3:] == 'sql' and f not in exclude]

    conn, cur = connect(os.path.join(location), debug=True)

    sql = '''
        SELECT filename
        FROM schema_changes
        ORDER BY executed asc;
    '''

    cur.execute(sql)
    res = cur.fetchall()
    executed = [i['filename'] for i in res]

    for file in files:
        if file not in exclude and file not in executed:
            logging.info(f"Script: {file}")

            with open(os.path.join(SQL_LOCATION, file), 'r') as script:
                try:
                    cur.executescript(script.read())

                    query = '''
                        INSERT INTO schema_changes (filename, executed)
                        VALUES (:filename, datetime());
                    '''
                    cur.execute(query, {'filename' : file})

                    conn.commit()

                    logging.info("Script executed successfully.")
                except:
                    logging.exception("Error applying update.")
                    conn.rollback()

    conn.close()

def drop(location):
    try:
        os.remove(os.path.join(location))
    except OSError:
        pass

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
        logging.basicConfig(level=logging.INFO)

    logging.debug("Arguments:" + str(args))

    path = args['path'][0]

    if args['create']:
        create(os.path.join(path))
        logging.info(f"Created new database at {path}")

    if args['update']:
        update(os.path.join(path))
