import psycopg2
from psycopg2 import DatabaseError
from decouple import config


def get_connection():
    try:
        return psycopg2.connect(
            host =  config('PGHOST'),
            user = config('PGUSER'),
            password =  config('PGPASSWORD'),
            database = config('PGDATABASE')
        )
    except DatabaseError as ex:
        raise ex