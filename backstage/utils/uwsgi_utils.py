import time

table = 'uwsgi_vassals'

config = 'dummy text'
uid = 'nobody'
gid = 'nobody'

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
        q = "select * from %s where name = '%s'" % (table, inst.name)
        cur.execute(q)
        conn.commit()
        if cur.fetchone() != None:
            print '%s found in wsgi table.\nHint try restart() to force a re-start' % (inst.name)
            return
        q = "insert into %s (name,config,ts,uid,gid) values ('%s','%s',%s,'%s','%s')" % \
            (table, inst.name, config, ts, uid, gid)
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
        q = "SELECT * FROM %s WHERE name = '%s'" % (table, inst.name)
        cur.execute(q)
        res = cur.fetchone()
        conn.commit()
        if res is None:
            print 'Act %s is not running' % inst.name
            return
    except:
        raise
    try:
        q = "DELETE FROM %s WHERE name = '%s'" % (table, inst.name)
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
        q = "SELECT * FROM %s WHERE name ='%s'" % (table, inst.name)
        cur.execute(q)
        conn.commit()
        if cur.fetchone() == None:
            print '%s is not running. Attempting to start.' % inst.name
            start(inst)
            return
        ts = time.time()

        q = "UPDATE %s set ts = %s where name = '%s'" % (table, ts, inst.name)
        cur.execute(q)
        conn.commit()
        print 'submitted re-start request for %s' % inst.name
    except:
        print 'failed %s' % inst.name
        conn.rollback
