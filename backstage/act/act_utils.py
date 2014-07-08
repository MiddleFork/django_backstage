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
    acthome = os.path.join(venue.acts_root, actname)
    if os.path.exists(acthome):
        print 'A folder named %s already exists under %s' % (actname, venue.acts_root)
        return None

    try:
        os.mkdir(acthome)
        copy_act_skel(venue, venue.acts_root, actname)
        keyfile = 'backstage-%s-%s.id' % (venue.venue_name, actname )
        with open(os.path.join(acthome, '.LIVE', keyfile), 'w') as kf:
            kf.write('#%s' % keyfile)
        act = Act(venue, actname)
        s = 'created Backstage Act %s at %s\n' % (actname, acthome)
        s += 'using Act %s' % actname
        print s
        venue.get_acts()
        return act
    except:
        s = 'something went wrong creating act.\n'
        s += 'you need to clean up the garbage because i have yet to do that for you.\n'
        print s
        raise None


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

