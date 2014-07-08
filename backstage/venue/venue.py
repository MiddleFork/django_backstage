import os
import sys
import subprocess
import stat

from backstage.utils import uwsgi_portsniffer
from backstage.utils.uwsgi.uwsgi_utils import build_uwsgi
from backstage.db.db_utils import create_default

class Venue():
    """A backstage Venue is a specific local install of backstage."""

    def __init__(self, venue_home):
        """Venue folder structure must already exist before we can create and utilize
        a venue instance
        """
        venue_secret = os.path.join(venue_home, '.LIVE/backstage-venue.txt')
        if not os.path.exists(venue_secret):
            print 'Invalid Venue'
            print 'Hint: create a Venue first using backstage.shortcuts.new_venue'
            return None
        #so now we have a valid venue folder structure we can instantiate the object
        self.venue_home = venue_home.rstrip('/') # or it will play with the auto pathing
        self.venue_root, self.venue_name = os.path.split(self.venue_home)
        self.name = self.venue_name
        self.longname = 'backstage-%s' % self.venue_name
        self.acts_root = os.path.abspath(os.path.join(self.venue_home, 'acts'))
        self.dbname = self.longname.replace('-', '_')

        if not self.venue_home in sys.path:
            sys.path.insert(0, self.venue_home)
        if not self.venue_root in sys.path:
            sys.path.insert(0, self.venue_root)
        if not self.acts_root in sys.path:
            sys.path.insert(2, self.acts_root)
        self.settings = None
        self.acts = {}
        self.conn = None
        self.get_settings()
        self.get_acts()
        self.uwsgi_config, self.uwsgi_ini = build_uwsgi(self, 'venue')
        try:
            self.connect()
        except:
            print 'OK, continuing, you can create the database later'
        return

    def get_settings(self):
        """ import the venue's settings.py"""
        settings = None
        try:
            exec_string = 'from %s import settings' % self.venue_name
            exec exec_string
            self.settings = settings
            return True
        except:
            print 'error getting venue settings'
            raise

    def connect(self):
        """
        connect to the instance's default database
        @return:
        """
        from backstage.db.db_utils import connect_default
        self.conn = connect_default(self)

    def create_all_act_dbs(self):
        for actname, actinstance in self.acts.iteritems():
            a = actinstance
            try:
                create_default(a)
            except:
                pass
        self.connect_all_act_dbs()

    def connect_all_act_dbs(self):
        """
        try to connect to all act databases
        @return:
        """
        act_connections = {}
        for k, v in self.acts.iteritems():
            name = k
            instance = v
            try:
                instance.connect()
                act_connections[name] = instance.conn.dsn
            except:
                act_connections[name] = None
        self.act_connections = act_connections
        return

    def dumpsettings(self):
        try:
            outfile = os.path.join(self.venue_home, 'settings_dump.py')
            of = open(outfile, 'w')
            my_settings = dir(self.settings)
            for my_setting in my_settings:
                s = "%s = my_settings['%s']\n" % (my_setting, my_setting)
                of.write(s)
            of.close()
        except:
            err = 'ERROR dumping settings'
            raise
        return True

    def build_virtualenv(self):
        """build the virtual environment for this backstage venue"""
        cwd = os.getcwd()
        venvdir = os.path.join(self.venue_home, 'venv')
        cmd = '%s/build_virtualenv' % (venvdir)
        st = os.stat(cmd)
        os.chmod(cmd, st.st_mode | stat.S_IEXEC)
        os.chdir(venvdir)
        subprocess.call(cmd)
        os.chdir(cwd)
        return

    def get_uwsgi_port(self):
        self.uwsgi_ip, self.uwsgi_port = uwsgi_portsniffer.get_uwsgi_port(self)
        return

    def reload(self):
        """Reload the Venue, by touching its ini file"""
        try:
            with file(self.uwsgi_ini, 'a'):
                os.utime(self.uwsgi_ini, None)
        except IOError:
            print 'Could not update, permission denied.'
            return
        self.get_uwsgi_port()
        return

    def get_acts(self):
        """get this Venue's Acts and find out about them"""
        from backstage.shortcuts import Act
        acts_list = os.listdir(self.acts_root)
        for a in acts_list:
            test_act = Act(self, a)
            try:
                if 'keyfile' in test_act.__dict__:
                    self.acts[a] = test_act
                else:
                    pass
            except:
                pass

    def __unicode__(self):
        s = 'Backstage Venue instance %s at %s' % (self.venue_name, self.venue_root)
        return s

    def start_all_acts(self):
        for act in self.acts.values():
            act.start()

    def stop_all_acts(self):
        for act in self.acts.values():
            act.stop()

    def restart_all_acts(self):
        for act in self.acts.values():
            act.restart()