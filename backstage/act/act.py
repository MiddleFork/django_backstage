import os
import sys
import time
import requests

from backstage.utils import uwsgi_portsniffer
from backstage.utils.uwsgi.uwsgi_utils import build_uwsgi

# Choose one of the below as the default uwsgi emperor vassal control:
from backstage.utils.uwsgi.linker_file_ini import start, stop, restart
#from backstage.utils.uwsgi.linker_pg_plugin import start, stop, restart


class Act():

    def __init__(self, venue, actname):
        acthome = os.path.join(venue.acts_root, actname)
        kf = 'backstage-%s-%s.id' % (venue.venue_name, actname)
        keyfile = os.path.join(acthome, '.LIVE', kf)
        if not os.path.exists(keyfile):
            #not a valid act
            return
        self.venue = venue
        self.actname = actname
        self.name = self.actname
        self.acthome = acthome
        self.longname = 'backstage-%s-%s' % (self.venue.name, self.name)
        self.keyfile = keyfile
        self.conn = venue.conn
        self.get_settings()
        self.uwsgi_config, self.uwsgi_ini = build_uwsgi(self, 'act')
        inifile = '%s.ini' % self.longname
        self.uwsgi_file = os.path.join(self.acthome, inifile)
        self.uwsgi_vassal = os.path.join(self.settings.UWSGI_VASSALS, inifile)
        #necessary for file-based uwsgi linking
        self.uwsgi_ip = None
        self.uwsgi_port = None
        if not os.path.exists(self.uwsgi_file):
            with open(self.uwsgi_file, 'w') as f:
                f.write(self.uwsgi_ini)

    def start(self):
        start(self)

    def stop(self):
        stop(self)

    def restart(self):
        restart(self)

    def get_settings(self):
        syspath = sys.path
        sys.path.insert(0, os.path.join(self.venue.venue_home, 'acts'))
        settings = None
        exec('from %s import settings' % self.actname)
        sys.path = syspath
        self.settings = settings
        return


    def get_uwsgi_log(self):
        fo = open(self.uwsgifile, 'r')
        d = fo.readlines()
        fo.close()
        logfile = None
        for line in d:
            line = line.strip()
            if line[0:9] == 'daemonize':
                logfile = line.split('=')[1]
                return logfile
        return logfile

    def get_uwsgi_port(self):
        """Get the uwsgi port using lsof.  Requires that lsof and fuser be suid root"""
        start_port =self.uwsgi_port
        timeout = 10
        nap = 1
        starttime = time.time()
        elapsed = 0
        valid = False
        while not valid and elapsed < timeout:
            try:
                fullport = uwsgi_portsniffer.port_from_lsof(self)
                new_ip, new_port = fullport.split(':')
                if new_port <> start_port:
                    self.uwsgi_ip = new_ip
                    self.uwsgi_port = new_port
                    print 'OK %s:%s' % (new_ip,new_port)
                    valid = True
            except:
                pass
            if not valid:
                time.sleep(nap)
                elapsed = time.time() - starttime
        return

    def connect(self):
        """
        connect to the instance's default database
        @return:
        """
        from backstage.db.db_utils import connect_default
        conn = connect_default(self)

    def sniff_uwsgi_port(self):
        """sniff the uwsgi port from the log file. inefficient but does not require
        root access"""
        ip, port = uwsgi_portsniffer.portsniffer(self.uwsgi_log)
        if port is None:
            print "No port.  Try self.uwsgi_linker(linkmode='link')"
            return
        uwsgi_uri = 'http://%s:%s' % (ip, port)
        try:
            h = requests.head(uwsgi_uri)
            if h.status_code == 200:
                self.uwsgi_ip = ip
                self.uwsgi_port = port
                print str(ip), str(port)
            else:
                print 'request for %s resulted in a status code of %s' % (uwsgi_uri, h.status_code)
                print 'the entire header follows:'
                print h
                if h.status_code == 500:
                    s = 'A status code of 500 means that the port is bound OK but that '
                    s+= 'there is probably a coding error somewhere in the Act '
                    s+= 'which is causing it to fail to load. '
                    s+= 'In your browser - and with DEBUG enabled, visit %s and review the error message' % (uwsgi_uri)
                    print s
                self.uwsgi_ip = None
                self.uwsgi_port = None
        except requests.exceptions.ConnectionError:
            s= 'Failure to load the URI at %s' % (uwsgi_uri)
            s+= 'Hint: this is probably a stale port.\nTry reloading the Act by touching its .ini file.\n'
            s+= 'Or, wait a few more seconds and try "(self).get_uwsgi_port() again'
            print s

            self.uwsgi_ip = None
            self.uwsgi_port = None
            print 'None'
        return