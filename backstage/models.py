from django.db import models


class Act(models.Model):
    """An Act is essentially a runnable Django application.   (Runnable, not necessarily Running.)
    The analogy is a musical Act (performer, ensemble, group, etc.)"""

    def __init__(self):
        pass

    def __unicode__(self):
        s = ''
        return s

    class Manager:
            """Naturally, an Act must have a Manager (act.manager).
            Think:  Reuben Kincaid (The Partridge Family), Colonel Tom arker (Elvis)."""

            def __init__(self):
                pass

class Stage(models.Model):
    """A Stage is an environment in which your Act can run,
    just as a musical Stage is a physical space where an Act can play music.
    Here, we will build and use a stage using Virtualenv, uWsgi and Nginx,
    though we could conceivably fashion a stage using gunicorn/supervisor or something else.
    """

    class Manager:
        """Our Stage Manager (stage.manager) works with the uWsgi Emperor to start/stop/add/remove/modify Sess(ion)s.
        Internally, that means working with Apps' uwsgi.ini files;
        externally, that means the StageManager needs elevated system-level privileges to add/remove links to
        /etc/uwsgi-emperor/vassals.
        A properly designed naming scheme for uwsgi.ini files/links will minimize chances for conflicts
        with other running Backstage instances (Productions).
        """

        def __init__(self):
            pass

    class Set(models.Model):
        """A Stage Set (stage.set) is the collection of installed apps (instruments),
        styles, scripts (lights and props, etc)
        """

        def __init__(self):
            pass

    def __init__(self):
        pass

    def __unicode__(self):
        s = ''
        return s


class Sess(models.Model):
    """A Sess (Session) is an Act playing on a Stage.  It's a Django App running under uWsgi.
    It exposes a port and/or socket on the local host.  It's like jamming in the garage.

    Sure you're playing music,
    but (aside from the angry neighbors) nobody in the external world hears or knows about it.
    (We use the diminutive 'Sess' instead of 'Session' to avoid conflict with Django Sessions).
    """

    def __init__(self):
        pass

    def __unicode__(self):
        s = ''
        return s


class Venue(models.Model):
    """A Venue is a DNS namespace, such as example.com, or private equivalent. A Venue itself is content-agnostic.
    If you want, it could display pictures of kittens (if you have a kittens Act)
    or it could display cupcake recipes (if you have a cupcakes Act).
    It may contain no content (no Booked Act).

    In the musical world, a Venue is a (public or private) location where people may go to listen to music.
    Depending on the Act, it could be Jazz on Friday and HipHop on Saturday.  It could be closed on Sunday (no content).
    """

    def __init__(self):
        pass

    def __unicode__(self):
        s = ''
        return s


class Gig(models.Model):
    """A Gig is a live running website.  It is an Act, Booked and playing a Sess on Stage at a Venue.
    It is "Live And In Concert."""

    def __init__(self):
        pass

    def __unicode__(self):
        s = ''
        return s


class Production(models.Model):
    """A Production is a single Backstage instance and the superset of its content."""

    class Manager:
        """The Production Manager has control over the entire Production.
        Notably, coordinates the activities of the Act, Stage and Booking Managers.
        An Act doesn't even get to play a jam Sess(ion), let alone have a Gig at a Venue,
        unless and until the Production Manager says so. """

        def __init__(self):
            pass

    def __init__(self):
        pass

    def __unicode__(self):
        s = ''
        return s
