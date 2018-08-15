import os
import psycopg2
from psycopg2 import sql

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
curs=conn.cursor()
def dbDump(table,data,col):
    q1 = sql.SQL("insert into {} ({}) values ({})").format(sql.Identifier(table),sql.SQL(', ').join(map(sql.Identifier, col)),sql.SQL(', ').join(sql.Placeholder() * len(col)))

    try:
        curs.execute(q1,data)
    except:
        conn.rollback()
    else:
        conn.commit()

def dbGet(table,col):
    q1=sql.SQL("SELECT {} FROM {}").format(sql.Identifier(col),sql.Identifier(table))
    
    try:
        curs.execute(q1)
    except:
        conn.rollback()
    else:
        data=curs.fetchall()
        return data

def dbrandGet(table,col):
    q1=sql.SQL("SELECT {} FROM {} ORDER BY RANDOM() LIMIT 1").format(sql.Identifier(col),sql.Identifier(table))
    str=''
    try:
        curs.execute(q1)
    except:
        conn.rollback()
    else:
        str=curs.fetchone()[0]
    return str