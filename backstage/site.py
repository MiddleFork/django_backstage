import os
from pwd import getpwnam
import shutil
import backstage

class Site():
    def __init__(self, project_instance, sitename):
        """ initialize a site instance, populate it if it doesn't exist """
        if not isinstance(project_instance, backstage.Project):
            s = 'The first argument must be an instance of a backstage project'
            print s
            raise
        if not isinstance(sitename, str):
            s = 'The second argument must be the name identifying the site'
            print s
            raise
        self.project = project_instance
        self.projectfolder = self.project.settings.PROJECT_ROOT
        #self.PROJECT_NAME = self.project.settings.PROJECT_NAME
        self.sitename = sitename
        self.sitepath = os.path.join(self.projectfolder, 'sites')
        self.sitefolder = os.path.join(self.sitepath, self.sitename)
        self.test_existance()
        if not self.exists:
            s = 'Site %s does not exist in project %s' % (self.sitename,self.project.PROJECT_NAME)
            print s
            raise
            #self.create()
            #self.populate()
            #self.applyparams('ALL')
            #self.getsettings()
        self.getsettings()
        self.getparams()

    def getparams(self):
        """ get site parameters from database """
        conn = self.project.conn
        cur = conn.cursor()
        q = "select id,name,domain,alldomains,gunicorn_port,site_db,maintheme,prettyname "
        q += "from django_site where name = '%s'" % (self.sitename)
        cur.execute(q)
        r = cur.fetchone()
        if r is None:
            print 'ERROR site %s not found in database' % (self.sitename)
            raise
        self.id = r[0]
        self.domain = r[2]
        self.alldomains = r[3]
        self.server_port = r[4]
        self.site_db = r[5]
        self.maintheme = r[6]
        self.prettyname = r[7]
        self.params = {
            'site_id': self.id,
            'site_name': str(self.sitename),
            'server_name': str(self.domain),
            'server_port': self.server_port,
            'site_db': str(self.site_db),
            'maintheme': str(self.maintheme),
            'prettyname': str(self.prettyname)
        }

    def changetheme(self, theme=None):
        """ choose a new theme, update the database,
        and re-write site_settings.py """
        if theme is None:
            print 'Theme name required.'
            return False
        if not theme in self.project.themes:
            print 'Theme not found, choices are %s' % str(self.project.themes)
            return False
        conn = self.project.conn
        cur = conn.cursor()
        q = "update django_site set maintheme = '%s' " % (theme)
        q += " where name = '%s'" % (self.sitename)
        cur.execute(q)
        try:
            conn.commit()
        except:
            print 'You do not have permission to do that to the database'
            return False
        self.params['maintheme'] = theme
        theme_settings = os.path.join(self.sitefolder, 'theme_settings.py')
        f = open(theme_settings, 'w')
        f.write("MAINTHEME='%s'\n" % (theme))
        f.close()

    def populate(self, replace=False):
        """ populate a site with content from the skel"""
        skel = os.path.join(self.projectfolder, 'skel/site/')
        for path, dirs, files in os.walk(skel):
            for the_dir in dirs:
                localpath = os.path.join(path.replace(skel, ''), the_dir)
                outfolder = os.path.join(self.sitefolder, localpath)
                if not os.path.exists(outfolder):
                    os.mkdir(outfolder)
            for thefile in files:
                localpath = os.path.join(path.replace(skel, ''), thefile)
                infile = os.path.join(skel, localpath)
                #all infiles have '.src' appended to their file name
                infile += ('.src')
                outfile = os.path.join(self.sitefolder, localpath)
                if replace or not os.path.exists(outfile):
                    shutil.copy(infile, outfile)
                    if localpath in self.project.paramfiles:
                        self.applyparams(localpath)
                    print outfile
                else:
                    print 'skipping %s' % (outfile)
            # build links FROM the site to the location on the system
        self.linkconf()
        # build links FROM the log files to the site (for convenience)
        self.logfiles()
        # create the MEDIA_ROOT if necessasary
        self.mediaroot()

    def mediaroot(self):
        """ create or set the MEDIA_ROOT folder"""
        from backstage.settings.static_settings import MEDIA_ROOT_BASE, WEBUSER

        p = os.path.join(MEDIA_ROOT_BASE, self.sitename)
        if not os.path.exists(p):
            os.mkdir(p)
        uid = getpwnam(WEBUSER).pw_uid
        gid = getpwnam(WEBUSER).pw_gid
        os.chown(p, -1, gid) # change the group to WEBUSER (ie www-data)
        os.chmod(p, 0775)

    def linkconf(self):
        """ build symlinks to the site conf files from locations on the file system
        /etc/nginx/sites-available & enabled; /etc/supervisor/conf.d
        """
        #supervisor
        local = os.path.join(self.sitefolder, 'conf/supervisor.conf')
        remote = '/etc/supervisor/conf.d/%s.conf' % (self.sitename)
        os.path.exists(remote) and os.unlink(remote) #remove if exists
        os.symlink(local, remote)
        #nginx
        local = os.path.join(self.sitefolder, 'conf/nginx.conf')
        remote = '/etc/nginx/sites-available/%s' % (self.sitename)
        e_remote = '/etc/nginx/sites-enabled/%s' % (self.sitename)
        os.path.exists(remote) and os.unlink(remote) #remove if exists
        os.symlink(local, remote)
        os.path.exists(e_remote) and os.unlink(e_remote)
        os.symlink(remote, e_remote)

    def applyparams(self, f=None):
        """ re-write a site's skel file applying the site's parameters """
        if f is None:
            print 'file name required'
            return False
        if f == 'ALL':
            files = self.project.paramfiles
        else:
            files = [f, ]
        for f in files:
            thefile = os.path.join(self.sitefolder, f)
            if not os.path.exists(thefile):
                print 'file %s not found' % (thefile)
                return False
            text = open(thefile, 'r').read() % self.params
            o = open(thefile, 'w')
            o.write(text)
            o.close()

    def getsettings(self):
        """ import the site's settings.py """
        try:
            exec_string = "from %s.sites.%s import settings" % (self.project.PROJECT_NAME, self.sitename)
            exec(exec_string)
            self.settings = settings
            return True
        except:
            return False

    def test_existance(self):
        """ test if a site exists """
        if os.path.exists(self.sitefolder):
            self.exists = True
        else:
            self.exists = False
        return self.exists

    def create(self):
        """create the site folder and then populate its original content"""
        if not self.exists:
            try:
                os.mkdir(self.sitefolder)
                self.exists = True
                print 'created'
            except:
                print 'failed'
                return False
        else:
            print 'exists'
            return False

    def copyskelfile(self, f=None, replace=False):
        """ replace a site's file with the skeleton version """
        if f is None:
            print 'file name required'
            return False
        infile = os.path.join(self.projectfolder, 'skel/site', f)
        infile += '.src'
        if not os.path.exists(infile):
            print 'file %s not found' % (infile)
            return False
        outfile = os.path.join(self.sitefolder, f)
        if not os.path.exists(outfile) or replace == True:
            shutil.copy2(infile, outfile)
            print outfile
            if f in self.project.paramfiles:
                self.applyparams(f)
        else:
            print 'skipping %s' % outfile

    def logfiles(self):
        """ create symlinks in the log folder for the logs """
        log_files = {
            'gunicorn.log': '/var/log/gunicorn/%s.log' % (self.sitename),
            'supervisor.log': '/var/log/supervisor/%s.log' % (self.sitename),
            'supervisor-err.log': '/var/log/supervisor/%s-err.log' % (self.sitename),
            'nginx.log': '/var/log/nginx/%s.log' % (self.sitename),
            'nginx-err.log': '/var/log/nginx/%s.error.log' % (self.sitename)
        }
        for k, v in log_files.iteritems():
            k = os.path.join(self.sitefolder, 'log', k)
            try:
                os.remove(k) # remove if exists
            except:
                pass
            os.symlink(v, k)

    def publish_to_web(self, host_key):
        """ (Not implemented)  publish the site to a specific www host by manipulating the nginx and powerdns tables
        @param host_nickname: lookup key for the host(s) we want to publish to.
        @return: boolean
        """
        return False
