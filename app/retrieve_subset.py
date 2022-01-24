#!/usr/bin/python3
import os
import argparse
from stockDB import StockDB

# Get three args {{POSTGRES_USER}} {{POSTGRES_PASSWORD}} {{POSTGRES_DB}}
parser = argparse.ArgumentParser()
parser.add_argument("-U", "--user", help="Type your DB user", required=True)
parser.add_argument("-P", "--password", help="Type your DB user\'s password", required=True)
parser.add_argument("-D", "--db", help="Type your DataBase name", required=True)
parser.add_argument("-H", "--host", help="DB server host name")
parser.add_argument("-F", "--filename", help="Your filename for saving generated.csv file", default="./data/gathered_data.csv")
args = parser.parse_args()


stockdb = StockDB(args.user, args.password, args.db, db_host=args.host)
stockdb.connect_db()

# Check existing tables
# stockdb.exec_query("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")


# Simple query... but we need copy_expert to save a file.
# stockdb.exec_query('''select * from students limit 10;''')

sql = """
    COPY (
        select * from stocks limit 10
    ) TO STDOUT WITH CSV HEADER
"""

with open(args.filename, 'w') as fp:
    stockdb.cursor.copy_expert(sql, fp)