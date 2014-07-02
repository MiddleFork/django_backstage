import os
import sys

from venue.venue import Venue
import backstage


def copy_venue_skel(venue_path):
    """Populate a (usually) new backstage venue with the contents of backstage/skel"""
    skeldir = os.path.join(os.path.dirname(backstage.__file__), 'skel/venue')
    if not os.path.exists(skeldir):
        s = 'Source skeleton files for backstage venue not found.  This is a system error'
        print s
        raise
    try:
        #Copy the contents of the 'skel' folder into the venue root
        os.system("cp -rpv %s/* %s" % (skeldir, venue_path))

    except:
        s = "ERROR copying the venue skel into %s" % venue_path
        print s
        raise
    return True


def create_venue_uwsgi_file(venue_base, venue_root, venue_name):
    """create the uwsgi ini file for a (usually) new Venue.
    Reads backstage/config/uwsgi.venue.ini.src
    """
    srcfile = os.path.join(os.path.dirname(backstage.__file__), 'conf/uwsgi.venue.ini.src')
    with open(srcfile, 'r') as f:
        srcdata = f.read()
    outfile = os.path.join(venue_root, 'backstage-%s-uwsgi.ini' % venue_name)
    o = open(outfile, 'w')
    o.write(srcdata.format(VENUE_BASE=venue_base, VENUE_ROOT=venue_root, VENUE_NAME=venue_name))
    o.close()
    return


def new_venue(venue_name, venue_base, source_ini_file = None):
        """create a new backstage venue with the given name and located at the specified path"""
        venue_path = os.path.abspath(os.path.join(venue_base, venue_name))
        try:
            os.makedirs(venue_path)
        except:
            print 'Error creating venue.'
            raise

        try:
            with open(os.path.join(venue_path, '__init__.py'), 'w'):
                pass
        except:
            err = 'ERROR with init file'
            print err
            raise
        try:
            copy_venue_skel(venue_path)
        except:
            s = 'Error in copy_venue_skel'
            print s
            raise

        try:
            create_venue_uwsgi_file(venue_base, venue_path, venue_name)
        except:
            s = 'Error in create_venue_wsgi_file'
            print s
            raise


        try:
            p = use_venue(venue_path)
        except:
            raise

        p.build_virtualenv()
        s = 'Successfully created Backstage venue %s at %s' % (p.VENUE_NAME, p.VENUE_ROOT)
        print s
        return p


def test_venue_exists(venue_root):
    """Test for the existence of a Backstage venue instance.  Return True or False"""
    if not os.path.exists(venue_root):
        s = 'venue folder at %s does not exist. Terminating' % venue_root
        print s
        return False
    #A file named backstage.ini should exist.  Proves this is a backstage venue.  Right now it is empty
    ini_file = os.path.join(venue_root, 'backstage.ini')
    if not os.path.exists(ini_file):
        s = 'Backstage INI file not found'
        print s
        return False
    return True


def use_venue(venue_root):
    """Use an existing Backstage venue.  Returns the venue instance."""
    exists = test_venue_exists(venue_root)
    if not exists:
        s = 'venue does not exist'
        print s
        raise

    try:
        backstage_venue = Venue(venue_root)
    except:
        raise
    paths = [backstage_venue.VENUE_ROOT, backstage_venue.VENUE_PATH, ]
    for pth in paths:
        if not pth in sys.path:
            sys.path.append(pth)
    try:
        backstage_venue.get_settings()
    except:
        s = 'Could not import settings'
        print s
        raise
    # paramfiles are those with parameterized variables needing to be replaced using the params dict.
    backstage_venue.paramfiles = ['site_settings.py', 'theme_settings.py', 'wsgi.py', 'conf/gunicorn_launcher',
                   'conf/nginx.conf', 'templates/index.html',
                   'conf/supervisor.conf', ]
    # this would be better in a db table
    backstage_venue.themes = ['default', 'default24', 'fluid', 'container', 'hero', ]
    try:
        backstage_venue.connect()
    except:
        s = 'Could not connect to database'
        raise
    s = 'Using Backstage venue %s at %s' % (backstage_venue.VENUE_NAME, backstage_venue.VENUE_ROOT)
    print s
    return backstage_venue


def venue_from_cwd():
    cwd = os.getcwd()
    try:
        v = Venue(cwd)
    except:
        v = None
    return v

