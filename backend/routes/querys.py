from psycopg2 import connect
from environs import Env

def init_db():
    env = Env()
    conn = connect(
        dbname='tarea1',
        user='postgres',
        password='postgres',
        host='postgres',
        port='5432'
    )
    return conn