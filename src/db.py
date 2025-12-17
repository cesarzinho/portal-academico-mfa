import os
import psycopg2
from contextlib import contextmanager

@contextmanager
def get_conn():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    try:
        yield conn
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        conn.close()
