#! /usr/bin/python

"""
database-check.py

This script will check whether the postgres container is up and running. It'll
connect to the database with the credentials provided in the environment
variables.
"""

import os
import sys
import psycopg2


def database_check():
    try:
        str = "dbname=" + os.environ.get('DB_NAME') + " user=" + os.environ.get('POSTGRES_USER') + " password=" + os.environ.get('POSTGRES_PASSWORD') + " host=" + os.environ.get('POSTGRES_HOST') + " port=" + os.environ.get('POSTGRES_PORT')
        psycopg2.connect(str)
    except:
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    database_check()