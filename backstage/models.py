import os
import sys
import time

import requests

#from django.db import models
from django.db.models.signals import pre_init, post_init
from Venue.venue import Venue
from backstage.utils import uwsgi_portsniffer


class Act(models.Model):
    actname = models.TextField(max_length=80)
    venue = models.ForeignKey(Venue)

    def reload(self):
        """Reload the Act, by touching its ini file"""
        try:
            with file(self.uwsgifile, 'a'):
                os.utime(self.uwsgifile, None)
        except IOError:
            print 'Could not update, permission denied.'
            return
        self.get_uwsgi_port()
        return

    def get_settings(self):
        syspath = sys.path
        sys.path.insert(0,os.path.join(self.venue.VENUE_ROOT,'acts'))
        exec('from %s import settings' % self.actname)
        sys.path = syspath
        settings = None
        self.settings = settings

    def uwsgi_linker(self, linkmode=None):
        """Links the uwsgi.ini file to the uwsgi emperor's vassals directory
        (set in backstage.backstage_settings UWSGI_VASSALS)
        """
        linkmodes = [None, 'link', 'unlink', 'relink']
        #vassal_name = 'backstage-%s-acts-%s.ini' % (self.venue.VENUE_NAME, self.actname)
        self.vassal_file = os.path.join(self.settings.UWSGI_VASSALS, self.uwsgifile)
        if linkmode not in linkmodes:
            return 'Usage: uwsgi_linker <%s>' % (linkmodes)
        if linkmode == None:
            pass
        elif linkmode == 'link':
            os.symlink(self.uwsgifile, self.vassal_file)
            self.get_uwsgi_port()
        elif linkmode == 'unlink':
            os.unlink(self.vassal_file)
            self.uwsgi_port = None
        elif linkmode == 'relink':
            os.unlink(self.vassal_file)
            self.uwsgi_port = None
            os.symlink(self.uwsgifile, self.vassal_file)
            self.get_uwsgi_port()

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
                fullport = uwsgi_portsniffer.port_from_lsof(self.vassal_file)
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

def prevalidate_venue(sender, **kwargs):
    """
    :param sender:
    :param kwargs:
    :return:
    Before we initialize a Venue we validate that it exists on the file system and in the db

    """
    print 'not so fast buddy.'


def postpopulate_venue(sender, **kwargs):
    """populate the venue upon its instantiation
    whether new or per-existent
    """
    venue = kwargs['instance']
    print venue.venue_name


def prevalidate_act(sender, **kwargs):
    """
    Pre-validate an act instance
    @param sender: vessel for passing the venue instance
    @param kwargs: 'instance' contains the venue instance
    @return:
    """
    act = kwargs['instance']
    act.acthome = os.path.join(act.venue.VENUE_ROOT, 'acts', act.actname)
    act.uwsgi_ip = None
    act.uwsgi_port = None
    act.uwsgifile = os.path.join(act.acthome, 'uwsgi.ini')
    if not os.path.exists(act.acthome):
        print 'Act %s does not exist in venue %s' % (act.venue.VENUE_NAME, act.actname)
        raise
    return

def postpopulate_act(sender, **kwargs):
    """
    Populate an act instance with some parameters and methods
    @param sender:
    @param kwargs:
    @return:
    """
    act = kwargs['instance']
    act.get_settings()
    act.uwsgi_linker()
    act.uwsgi_log = act.get_uwsgi_log()
    return

#Execute upon initiation of Venue object.
#Populate some content for the venue
pre_init.connect(prevalidate_act, sender=Act)
post_init.connect(postpopulate_act, sender=Act)
pre_init.connect(prevalidate_venue, sender=Venue)
post_init.connect(postpopulate_venue, sender=Venue)