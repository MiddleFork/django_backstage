import os
import tarfile

import tempfile
import backstage
from backstage.shortcuts import Act, Venue
from backstage.venue.venue_utils import use_venue


def new_act(venue, actname):
    """create a new Act within a backstage Venue"""
    if isinstance(venue, str):
        try:
            venue = use_venue(venue)
        except:
            venue = None
    if not isinstance(venue, Venue):
        print '%s is not a valid backstage venue' % venue
        return None
    actsdir = os.path.join(venue.venue_home, 'acts')
    acthome = os.path.join(actsdir, actname)
    if os.path.exists(acthome):
        print 'A folder named %s already exists under %s' % (actname, actsdir)
        return None
    os.mkdir(acthome)
    copy_act_skel(venue, actsdir, actname)
    create_act_uwsgi_file(venue, actsdir, actname)

    act = Act(venue, actname)
    if act:
        s = 'created Backstage Act %s at %s' % (actname, acthome)
        print s
        s = 'using Act %s' % act
        print s
    return act

def create_act_uwsgi_file(venue, actsdir, actname):
    """create the uwsgi ini file for a (usually) new Act. This reads in backstage/conf/uwsgi.ini.src
    and substitutes values appropriately."""
    srcfile = os.path.join(os.path.dirname(backstage.__file__), 'conf/uwsgi.act.ini.src')
    with open(srcfile, 'r') as f:
        srcdata = f.read()
    outname = 'backstage-%s-%s.ini' % (venue.venue_name, actname)
    outfile = os.path.join(actsdir, actname, outname)
    o = open(outfile, 'w')
    o.write(srcdata.format(VENUE_ROOT=venue.VENUE_ROOT, VENUE_NAME=venue.VENUE_NAME, ACT_NAME=actname))
    o.close()
    return

def copy_act_skel(venue, actsdir, actname):
    """copy the skeleton files into the Act instance folder"""
    backstage_home = os.path.dirname(os.path.abspath(backstage.__file__))
    act_home = os.path.join(actsdir, actname)
    act_skel = os.path.join(backstage_home, 'skel/act')
    #recursive copy via tar
    tmpfile = tempfile.NamedTemporaryFile()
    tmpfile.close()
    tar_file = tarfile.open(tmpfile.name, 'w')
    cwd = os.getcwd()
    os.chdir(act_skel)
    tar_file.add('.')
    os.chdir(cwd)
    tar_file.close()
    tar_file = tarfile.open(tmpfile.name, 'r')
    tar_file.extractall(act_home)
    tar_file.close()
    os.remove(tmpfile.name)
