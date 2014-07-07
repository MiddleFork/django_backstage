"""
linker_pg_plugin.py
Creates vassals for the uWSGI emperor using the pg_emperor plugin.
defines start, stop, and restart functions.  Upstream classes such as Act
can choose which linker from which to load these (eg file:// vs pg_emperor, etc)
"""

import time
from backstage.utils.uwsgi.uwsgi_utils import table, uid, gid

def start(inst):
    try:
        conn = inst.conn
        cur = conn.cursor()
    except:
        try:
            conn = inst.venue.conn
            cur = conn.cursor()
        except:
            print 'connection error'
            return
    try:
        ts = time.time()
        q = "select * from %s where name = '%s.ini'" % (table, inst.name)
        cur.execute(q)
        conn.commit()
        if cur.fetchone() != None:
            print '%s found in wsgi table.\nHint try restart() to force a re-start' % (inst.name)
            return
        q = "insert into %s (name,config,ts,uid,gid) values ('%s.ini','%s',%s,'%s','%s')" % \
            (table, inst.name, inst.uwsgi_ini, ts, uid, gid)
        cur.execute(q)
        conn.commit()
        print 'start request submitted for %s' % inst.name
    except:
        raise
        print 'failed to start'
        conn.rollback
        return
    return


def stop(inst):
    try:
        conn = inst.conn
        cur = conn.cursor()
    except:
        try:
            conn = inst.venue.conn
            cur = conn.cursor()
        except:
            print 'connection error'
            return
    try:
        q = "SELECT * FROM %s WHERE name = '%s.ini'" % (table, inst.name)
        cur.execute(q)
        res = cur.fetchone()
        conn.commit()
        if res is None:
            print 'Act %s is not running' % inst.name
            return
    except:
        raise
    try:
        q = "DELETE FROM %s WHERE name = '%s.ini'" % (table, inst.name)
        cur.execute(q)
        conn.commit()
        print 'stop request submitted for %s' % inst.name
    except:
        print 'delete error %s' % inst.name
        conn.rollback()
    return


def restart(inst):
    try:
        conn = inst.conn
        cur = conn.cursor()
    except:
        try:
            conn = inst.venue.conn
            cur = conn.cursor()
        except:
            print 'connection error'
            return
    try:
        q = "SELECT * FROM %s WHERE name ='%s.ini'" % (table, inst.name)
        cur.execute(q)
        conn.commit()
        if cur.fetchone() == None:
            print '%s is not running. Attempting to start.' % inst.name
            start(inst)
            return
        ts = time.time()

        q = "UPDATE %s set ts = %s where name = '%s.ini'" % (table, ts, inst.name)
        cur.execute(q)
        conn.commit()
        print 'submitted re-start request for %s' % inst.name
    except:
        print 'failed %s' % inst.name
        conn.rollback