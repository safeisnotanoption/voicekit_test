"""Скрипт создаёт необходимые таблицы базы данных для работы нашего скрипта"""


import psycopg2
from psycopg2 import sql
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import config


user = config.PG_USER
password = config.PG_PASSWORD


def init_database():
    init_query = """
                 CREATE DATABASE {}
                 WITH 
                 OWNER = {}
                 ENCODING = 'UTF8'
                 LC_COLLATE = 'Russian_Russia.1251'
                 LC_CTYPE = 'Russian_Russia.1251'
                 TABLESPACE = pg_default
                 CONNECTION LIMIT = -1;
                 """
    conn = None
    try:
        conn = psycopg2.connect(dbname='postgres',
                                user=config.PG_USER,
                                password=config.PG_PASSWORD,
                                host=config.PG_HOST,
                                port=config.PG_PORT,
                                )

        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute(sql.SQL(init_query).format(
            sql.Identifier("voicekit_db"),
            sql.Identifier(user))
        )
    except psycopg2.errors.DuplicateDatabase:
        print("База данных 'voicekit_db' уже существует, пропускаем создание")
    except Exception as e:
        print(e)
    finally:
        conn.close()


def init_tables():
    init_query = """
                 CREATE TABLE IF NOT EXISTS project(
                         id SERIAL PRIMARY KEY,
                         name varchar(30),
                         description text
                 );
                 
                 CREATE TABLE IF NOT EXISTS server(
                         id SERIAL PRIMARY KEY,
                         name varchar(30),
                         ip_address text,
                         description text
                 );
                 
                 CREATE TABLE IF NOT EXISTS voice_call(
                     id SERIAL PRIMARY KEY,
                     datetime timestamp,
                     operation_id varchar(40),
                     result bool,
                     phone varchar(30),
                     duration real,
                     transcript text,
                     project_id integer REFERENCES project(id),
                     server_id integer REFERENCES server(id)
                 );
                 """
    conn = None
    try:
        conn = psycopg2.connect(user=config.PG_USER,
                                password=config.PG_PASSWORD,
                                host="127.0.0.1",
                                port="5432",
                                database="voicekit_db")
        cur = conn.cursor()
        cur.execute(init_query)
        conn.commit()
        cur.close()
        print("Создание таблиц успешно завершено")
    except Exception as e:
        print(e)
    finally:
        conn.close()


init_database()
init_tables()
