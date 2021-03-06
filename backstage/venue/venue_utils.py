import os
import sys

from backstage.shortcuts import Venue
import backstage


def copy_venue_skel(venue_home):
    """Populate a (usually) new backstage venue with the contents of backstage/skel"""
    skeldir = os.path.join(os.path.dirname(backstage.__file__), 'skel/venue')
    if not os.path.exists(skeldir):
        s = 'Source skeleton files for backstage venue not found.  This is a system error'
        print s
        raise
    try:
        #Copy the contents of the 'skel' folder into the venue root
        os.system("cp -rp %s/. %s" % (skeldir, venue_home))

    except:
        s = "ERROR copying the venue skel into %s" % venue_home
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


def new_venue(venue_name, venue_root, requirements_txt = None):
        """create a new backstage venue with the given name and located at the specified path.
        Optionally supply a valid requirements.txt file with which to populate the virtual environment"""
        venue_home = os.path.abspath(os.path.join(venue_root, venue_name))

        if requirements_txt is not None:
            try:
                fn = os.path.split(requirements_txt)[1]
                if not fn.startswith('requirements') or not fn.endswith('.txt'):
                    print 'Invalid Filename: %s' % fn
                    raise
                try:
                    f = open(requirements_txt)
                    f.close()
                except IOError:
                    print 'IO Error (hint: check for file)'
                    raise
            except:
                print 'Could not create venue'
                raise
                return None

        try:
            os.makedirs(venue_home)
        except:
            print 'Error creating venue (hint: check write access).'
            raise

        try:
            with open(os.path.join(venue_home, '__init__.py'), 'w'):
                pass
        except:
            err = 'ERROR with init file'
            print err
            raise
        try:
            copy_venue_skel(venue_home)
        except:
            s = 'Error in copy_venue_skel'
            print s
            raise

        try:
            create_venue_uwsgi_file(venue_root, venue_home, venue_name)
        except:
            s = 'Error in create_venue_wsgi_file'
            print s
            raise

        try:
            venue = use_venue(venue_home)
        except:
            raise

        venue.build_virtualenv(requirements_txt)
        s = 'Successfully created Backstage venue %s at %s' % (venue.venue_name, venue.venue_root)
        print s
        return venue


def test_venue_exists(venue_home):
    """Test for the existence of a Backstage venue instance.  Return True or False"""
    if not os.path.exists(venue_home):
        s = 'venue folder at %s does not exist. Terminating' % venue_home
        print s
        return False
    #A keyfile under .LIVE should exist.  Proves this is a backstage venue.  Right now it is empty
    keyfilename = 'backstage-venue.txt'
    keyfile = os.path.join(venue_home, '.LIVE', keyfilename)
    if not os.path.exists(keyfile):
        s = 'Backstage key file file not found'
        print s
        return False
    return True


def use_venue(venue_home):
    """Use an existing Backstage venue.  Returns the venue instance."""
    exists = test_venue_exists(venue_home)
    if not exists:
        s = 'Venue does not exist'
        raise s

    try:
        venue = Venue(venue_home)
        print venue
        dir(venue)
    except:
        print
        raise
    paths = [venue.venue_home, venue.venue_root, ]
    for pth in paths:
        if not pth in sys.path:
            sys.path.append(pth)
    try:
        venue.get_settings()
    except:
        s = 'Could not import settings'
        print s
        raise
    # paramfiles are those with parameterized variables needing to be replaced using the params dict.
    venue.paramfiles = ['site_settings.py', 'theme_settings.py', 'wsgi.py', 'conf/gunicorn_launcher',
                   'conf/nginx.conf', 'templates/index.html',
                   'conf/supervisor.conf', ]
    # this would be better in a db table
    venue.themes = ['default', 'default24', 'fluid', 'container', 'hero', ]
    try:
        venue.connect()
    except:
        s = 'Could not connect to database'
        raise
    s = 'Using Backstage venue %s at %s' % (venue.venue_name, venue.venue_root)
    print s
    return venue


def venue_from_cwd():
    cwd = os.getcwd()
    try:
        v = Venue(cwd)
    except:
        v = None
    return v

