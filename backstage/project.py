import os
import sys
import shutil
import backstage
import subprocess

class Project():
    """A backstage project is a specific local install of backstage."""
    def __init__(self,project_root):
        """Initialize a Backstage Project instance. Required arguments are the name of the project and the fullpath of the project (name included)
        """
        self.PROJECT_ROOT = os.path.abspath(project_root)
        self.PROJECT_PATH,self.PROJECT_DIRNAME = os.path.split(self.PROJECT_ROOT)
        self.PROJECT_NAME = self.PROJECT_DIRNAME

        #ensure that the project path is on sys.path
        self.PROJECT_PATH in sys.path or sys.path.insert(0,self.PROJECT_PATH)


    def __unicode__(self):
        s = 'Django Backstage project named %s at %s' % (self.PROJECT_NAME, self.PROJECT_PATH)
        return s

    def get_settings(self):
        """ import the project's settings.py"""
        try:
            exec_string = 'from %s import settings' % self.PROJECT_NAME
            print exec_string
            exec(exec_string)
            self.settings = settings
            return True
        except:
            raise

    def connect(self):
        """ connect to the project database """
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
    def getallsites(self):
        """ create a dictionary of all sites, from the database """
        self.sites = {}
        self.connect()
        cur = self.conn.cursor()
        q = 'select name,id,domain,alldomains,site_db,gunicorn_port from django_site where id <> 1'
        cur.execute(q)
        results = cur.fetchall()
        for r in results:
            self.sites[r[0]] = {
                'id': r[1],
                'domain': str(r[2]),
                'alldomains': str(r[3]),
                'site_db': str(r[4]),
                'gunicorn_port': r[5]
            }

    def buildallsites(self):
        """ for each site, create and populate (if necessary) """
        try:
            self.sites
        except:
            self.getallsites()
        skel = os.path.join(self.settings.PROJECT_ROOT, 'skel/site')
        for s in self.sites:
            site = backstage.Site(s)
            print 'Site:  %s' % (site.sitename)
            site.populate(replace=False)

    def copyskelfile(self, f=None, replace=False):
        """ replace a skel file into all sites """
        if f is None:
            print 'File Name Required.'
            return False
        infile = os.path.join(self.settings.PROJECT_ROOT, 'skel/site', f)
        infile += '.src'
        if not os.path.exists(infile):
            print 'source file %s not found' % (infile)
            return False
        try:
            self.sites
        except:
            self.getallsites()
        for s in self.sites:
            site = backstage.Site(s)
            site.copyskelfile(f, replace)

    def dumpsettings(self):
        try:
            outfile = os.path.join(self.PROJECT_ROOT,'settings_dump.py')
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

def copy_project_skel(project_dir):
    """Populate a (usually) new backstage project with the contents of backstage/skel"""
    skeldir = os.path.join(os.path.dirname(backstage.__file__),'skel')
    if not os.path.exists(skeldir):
        s = 'Source skeleton files for backstage project not found.  This is a system error'
        print s
        raise
    try:
        #Copy the contents of the 'base' folder into the project root
        skelbase=os.path.join(skeldir, 'base')
        os.system("cp -rpv %s/* %s" % (skelbase, project_dir))

    except:
        s = "ERROR copying the project skel into %s" % project_dir
        print s
        raise
    return True

def new_project(project_name, project_path, source_ini_file = None):
        """create a new backstage project with the given name and located at the specified path"""
        project_path = os.path.abspath(os.path.join(project_path, project_name))
        try:
            os.makedirs(project_path)
        except:
            print 'Error creating project.'
            raise

        try:
            with open(os.path.join(project_path, '__init__.py'), 'w'):
                pass
        except:
            err = 'ERROR with init file'
            print err
            raise
        try:
            if source_ini_file is not None:
                pass  #try to copy the file
            fh=open(os.path.join(project_path, 'backstage.ini'), 'w')
            fh.write('[backstage]\n')
            fh.close()
        except:
            print 'Error with INI file'
            raise

        try:
            copy_project_skel(project_path)
        except:
            s = 'Error in copy_project_skel'
            print s
            raise



        try:
            p = use_project(project_path)
        except:
            raise
        s = 'Successfully created Backstage project %s at %s' % (p.PROJECT_NAME, p.PROJECT_ROOT)
        print s
        return p

def test_project_exists(project_root):
    """Test for the existence of a Backstage Project instance.  Return True or False"""
    if not os.path.exists(project_root):
        s = 'Project folder at %s does not exist. Terminating' % project_root
        print s
        return False
    #A file named backstage.ini should exist.  Proves this is a backstage project.  Right now it is empty
    ini_file = os.path.join(project_root, 'backstage.ini')
    if not os.path.exists(ini_file):
        s = 'Backstage INI file not found'
        print s
        return False
    return True

def use_project(project_root):
    """Use an existing Backstage project.  Returns the Project instance."""
    exists = test_project_exists(project_root)
    if not exists:
        s = 'Project does not exist'
        print s
        raise

    try:
        backstage_project = Project(project_root)
    except:
        raise
    paths = [backstage_project.PROJECT_ROOT, backstage_project.PROJECT_PATH, ]
    for pth in paths:
        if not pth in sys.path:
            sys.path.append(pth)
    try:
        backstage_project.get_settings()
    except:
        s = 'Could not import settings'
        print s
        raise
    # paramfiles are those with parameterized variables needing to be replaced using the params dict.
    backstage_project.paramfiles = ['site_settings.py', 'theme_settings.py', 'wsgi.py', 'conf/gunicorn_launcher',
                   'conf/nginx.conf', 'templates/index.html',
                   'conf/supervisor.conf', ]
    # this would be better in a db table
    backstage_project.themes = ['default', 'default24', 'fluid', 'container', 'hero', ]
    try:
        backstage_project.connect()
    except:
        s = 'Could not connect to database'
        raise
    s = 'Using Backstage Project %s at %s' % (backstage_project.PROJECT_NAME, backstage_project.PROJECT_ROOT)
    print s
    return backstage_project

