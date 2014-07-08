__author__ = 'walker'
"""
db_utils
Utils for working with backstage databases
"""
import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.conf import settings
from django.core.management import call_command

def get_dsn(inst):
    """ build the psycopg2 connection dsn
    @param inst:
    @return:
    """
    try:
        if inst.dsn is not None and inst.dsn_backstage is not None:
            return inst.dsn, inst.dsn_backstage
    except:
        pass
    db = get_default_db(inst)
    #dsn for the default database
    dsn = "dbname=%s port=%s host=%s" % (db['NAME'], db['PORT'], db['HOST'])
    #dsn for the 'backstage' database
    dsn_backstage = "dbname=backstage port=%s host=%s" % (db['PORT'], db['HOST'])
    inst.dsn = dsn
    inst.dsn_backstage = dsn_backstage
    return dsn, dsn_backstage

def get_default_db(inst):
    """
    return the instance's default db
    @param inst:
    @return:
    """
    try:
        db = inst.settings.DATABASES['default']
        return db
    except:
        print 'error getting database'
        return None


def connect_default(inst):
    """
    Connect this instance to its default database, as defined in settings
    @param inst: Backstage Act or Venue instance
    @return:
    """
    try:
        dsn, dsn_backstage = get_dsn(inst)
        conn = psycopg2.connect(dsn)
        inst.conn = conn
        return conn
    except psycopg2.OperationalError, e:
        if 'does not exist' in str(e):
            s = str(e).replace('FATAL:', '').strip()
            s += '\nHint: try "backstage.db.db_utils.create_default()"'
            print s
            return None
        else:
            print e
            return

def sync_default(inst):

    """
    Sync the default database
    @param inst:
    @return:
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % inst.name)
    os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % inst.name
    call_command('syncdb', verbosity=0, interactive=False, settings='%s.settings' % inst.name)

def migrate_default(inst):
    """
    Migrate the default database
    @param inst:
    @return:
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', '%s.settings' % inst.name)
    os.environ['DJANGO_SETTINGS_MODULE'] = '%s.settings' % inst.name
    call_command('migrate', interactive=False, verbosity=0, settings='%s.settings' % inst.name)

def create_default(inst):
    """
    Create a backstage database for a given backstage instance
    @param inst:
    @return:
    """
    #first try to connect to it. fail if it already exists
    try:
        dsn, dsn_backstage = get_dsn(inst)
    except Exception, e:
        print 'Error getting the dsn info'
        print e
        raise
    try:
        conn = psycopg2.connect(dsn)
        if isinstance(conn, psycopg2._psycopg.connection):
            print 'Database already exists'
            return
    except: # failure to connect, ie we can continue
        pass
    #try to connect to the backstage database. necessary to
    #connect to an existing db before we can create this one
    try:
        conn = psycopg2.connect(dsn_backstage)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        db = get_default_db(inst)
        dbname = db['NAME']
        q = "CREATE DATABASE %s" % dbname
        cur.execute(q)
        conn.commit()
        cur.close()
        conn.close()
        print 'Successfully created Act database %s' % dbname
        return
    except Exception, e:
        print e
        raise
