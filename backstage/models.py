import os


#from django.db import models
from django.db.models.signals import pre_init, post_init
from act.act import Act
from venue.venue import Venue


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