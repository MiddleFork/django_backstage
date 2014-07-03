import time

table = 'uwsgi_vassals'

config = 'dummy text'
uid = 'backstage'
gid = 'adm'

uwsgi_defaults = {
    'master': 'True',
    'processes': '8',
    'http-socket': '127.0.0.1:0',
    'plugins': 'python',
    'harikiri': '20',
    'log-maxsize': '100000',
    'max-requests': '1000',
    'vacuum': 'True',
    'disable-logging': 'True',
    'uid': 'backstage',
    'gid': 'adm',
    }

venue_seeds = {
    'home': '{VENUE_HOME}/venv',
    'virtualenv': '{VENUE_HOME}/venv',
    'pythonpath': '{VENUE_HOME}',
    'chdir': '{VENUE_ROOT}',
    'module': '{VENUE_NAME}.wsgi:application',
    'pidfile': '{VENUE_HOME}/.LIVE/uwsgi-backstage-{VENUE_NAME}.pid',
    'socket': '{VENUE_HOME}/.LIVE/uwsgi-backstage-{VENUE_NAME}.sock',
    'daemonize': '/var/log/uwsgi/uwsgi-backstage-{VENUE_NAME}.log',
}

act_seeds = {
    'home': '{VENUE_HOME}/venv',
    'virtualenv': '{VENUE_HOME}/venv',
    'chdir': '{VENUE_HOME}/acts',
    'pythonpath': '{VENUE_HOME}/acts',
    'module': '{ACT_NAME}.wsgi:application',
    'pidfile': '{VENUE_HOME}/.LIVE/uwsgi-backstage-{VENUE_NAME}-{ACT_NAME}.pid',
    'socket': '{VENUE_HOME}/.LIVE/uwsgi-backstage-{VENUE_NAME}-{ACT_NAME}.sock',
    'daemonize': '/var/log/uwsgi/uwsgi-backstage-{VENUE_NAME}-{ACT_NAME}.log',
}





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


def format_act_options(act):
    opts = {}
    for k, v in act_seeds.iteritems():
        opts[k] = v.format(VENUE_HOME=act.venue.venue_home, VENUE_NAME=act.venue.name, ACT_NAME=act.name)
    return opts


def build_uwsgi_ini(obj, objtype):
    """
    build a string formatted like a uwsgi.ini file
    @return:
    """
    uwsgi_config = {}
    for k, v in uwsgi_defaults.iteritems():
        uwsgi_config[k] = v


    options = {
        'act': format_act_options,
        'venue': format_venue_options,
        }

    local_options = options[objtype](obj)
    for k, v in local_options.iteritems():
        uwsgi_config[k] = v

    uwsgi_ini = '[uwsgi]\n'
    for k, v in uwsgi_config.iteritems():
        uwsgi_ini += '%s = %s\n' % (k, v)
    return uwsgi_config, uwsgi_ini


def format_venue_options(venue):
    opts = {}
    for k, v in venue_seeds.iteritems():
        opts[k] = v.format(VENUE_HOME=venue.venue_home, VENUE_NAME=venue.venue_name, VENUE_ROOT=venue.venue_root)
    return opts