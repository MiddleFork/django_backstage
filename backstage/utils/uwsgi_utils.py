import psycopg2
import datetime
import time

port = 5433
host = 'skok'
db = 'backstage_nooksack'
password = 'shuksan'
user = 'walker'

conn = psycopg2.connect('dbname=%s host=%s port=%s user=%s password=%s' % (db, host, port, user, password))
cur = conn.cursor()

table='uwsgi_vassals'

actname = 'act1'
uid = 'backstage'
gid = 'adm'
config = 'dummy text'
ts = time.time()

def start(self):
    try:
        ts = time.time()
        q = "insert into %s (name,config,ts,uid,gid) values ('%s','%s',%s,'%s','%s')" % \
            (table, self.actname, config, ts, uid, gid)
        cur.execute(q)
        conn.commit()
        print 'started %s' % self.actname
    except:
        print 'failed %s' % self.actname
        conn.rollback

def stop(self):
    q = "DELETE FROM %s WHERE name = '%s'" % (table, self.actname)
    try:
        cur.execute(q)
        conn.commit()
    except:
        print 'delete error'
        conn.rollback()
    return


def restart(self):
    try:
        ts = time.time()
        q = "UPDATE %s set ts = %s where name = '%s'" % (table, ts, self.actname
            (table, self.actname, config, ts, uid, gid)
        cur.execute(q)
        conn.commit()
        print 're-started %s' % self.actname
    except:
        print 'failed %s' % self.actname
        conn.rollback
