__author__ = 'walker'
import psycopg2

def connect(dbname, dbport):
    try:
        dsn = 'dbname=%s port=%s' % (dbname, dbport)
        conn = psycopg2.connect(dsn)
        #print 'database connected: %s' % dsa
    except psycopg2.OperationalError:
            e = 'Error connecting to the database'
            conn = None
            raise e
    return conn



"""
try:
    db = self.settings.DATABASES['default']
    string = "dbname=%s host=%s port=%s user=%s " % \
            (db['NAME'],
            db['HOST'],
            db['PORT'],
            db['USER']
            )
"""