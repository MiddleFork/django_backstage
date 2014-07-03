import os
import subprocess
import stat
from backstage.utils import uwsgi_portsniffer

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
        self.venue_home = venue_home
        self.venue_root, self.venue_name = os.path.split(self.venue_home)

    def get_settings(self):
        """ import the venue's settings.py"""
        settings = None
        try:
            exec_string = 'from %s import settings' % self.venue_name
            exec exec_string
            self.settings = settings
            return True
        except:
            raise

    def connect(self):
        """ connect to the venue database """
        import psycopg2
        try:
            db = self.settings.DATABASES['default']
            string = "dbname=%s host=%s port=%s user=%s " % \
                     (db['NAME'],
                      db['HOST'],
                      db['PORT'],
                      db['USER']
                     )
            self.conn = psycopg2.connect(string)
            return True
        except:
            return False

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
        self.uwsgi_ip, self.uwsgi_port = uwsgi_portsniffer.get_uwsgi_port(self.uwsgi_ini)
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
        self.acts = {}
        acts_root = os.path.abspath(os.path.join(self.venue_home, 'acts'))
        acts_list = os.listdir(acts_root)
        for a in acts_list:
            try:
                act = Act(self, a)
                self.acts[a] = act
            except:
                pass


    def __unicode__(self):
        s = 'Backstage Venue instance %s at %s' % (self.venue_name, self.venue_root)
        return s