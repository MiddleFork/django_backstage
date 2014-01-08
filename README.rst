Django Backstage

In the early days of Django, running apps were very much tied to specific websites.

In order to make apps and pages reusable between websites, the Sites framework was integrated into Django.

This historically makes sense in the context of an Apache-modwsgi environment, which hardwired individual running Django apps to individual web domain names.

Jump ahead to today where the emerging recommended standard is uwsgi + nginx.   This is an era where your Django apps may be providing RESTful services, WebSockets, and any of a variety of other services, in additional to 'traditional' html/css/js content.

And thanks to uWsgi, you may have as many of these various services running on as many different ports (or sockets) as you wish, blissfully running along without the need for any additional webserver (goodby apache) whatsoever.

It is not until later (if at all) when we bind one of our happy little uWsgi services to a webserver (hello nginx - but more about that later) that we are in the logical realm of talking about 'sites' in the context of web domain names and the Sites framework.

Some may just be building blocks to larger services and not exposed in a public namespace so referring to them as Sites is clearly meaningless in this context.

We need a new way to talk about and manage these services.

So, we introduce here the Django Backstage project and use (and probably over-abuse) a Jazz metaphor to represent its structural and functional components:

class Act:
    """An Act is essentially a runnable Django application.   (Runnable, not necessarily Running.)  The analogy is a musical Act (performer, ensemble, group, etc.)  Miles Davis sometimes had the reputation of being reclusive. Davis may have gone periods between performances, but remained a musical Act all the while.   It's the existence, not their performance (in the case of musicians) that define them as Acts; likewise it is the existence of your app, not the fact that it is running, that defines it as an Act."""
    class Manager:
        """Naturally, an Act must have a Manager (act.manager).  Think:  Reuben Kincaid (The Partridge Family), Colonel Tom Parker (Elvis).

class Stage:
    """A Stage is an environment in which your Act can run, just as a musical Stage is a physical space where an Act can play music.  Here, we will build and use a stage using Virtualenv, uWsgi and Nginx, though we could conceivably fashion a stage using gunicorn/supervisor or something else.
"""
    class Manager:
        """Our Stage Manager (stage.manager) works with the uWsgi Emperor to start/stop/add/remove/modify Sess(ion)s.  Internally, that means working with Apps' uwsgi.ini files; externally, that means the StageManager needs elevated system-level privileges to add/remove links to /etc/uwsgi-emperor/vassals.   A properly designed naming scheme for uwsgi.ini files/links will minimize chances for conflicts with other running Backstage instances (Productions).
"""
    class Set:
        """A Stage Set (stage.set) is the collection of installed apps (instruments), styles, scripts (lights and props, etc)"""

class Sess:
        """A Sess (Session) is an Act playing on a Stage.  It's a Django App running under uWsgi. It exposes a port and/or socket on the local host.  It's like jamming in the garage.  Sure you're playing music, but (aside from the angry neighbors) nobody in the external world hears or knows about it.  (We use the diminutive 'Sess' instead of 'Session' to avoid conflict with Django Sessions).
"""

class Venue:
        """A Venue is a DNS namespace, such as example.com, or private equivalent. A Venue itself is content-agnostic.  If you want, it could display pictures of kittens (if you have a kittens Act) or it could display cupcake recipes (if you have a cupcakes Act).  It may contain no content (no Booked Act).  In the musical world, a Venue is a (public or private) location where people may go to listen to music.  Depending on the Act, it could be Jazz on Friday and HipHop on Saturday.  It could be closed on Sunday (no content).
"""

class Gig:
"""A Gig is a live running website.  It is an Act, Booked and playing a Sess on Stage at a Venue.   It is "Live And In Concert."
"""

class Production:
"""A Production is a single Backstage instance and the superset of its content."""
    class Manager:
        """The Production Manager has control over the entire Production.  Notably, coordinates the activities of the Act, bcegmnqrstuvxStage and Booking Managers.   An Act doesn't even get to play a jam Sess(ion), let alone have a Gig at a Venue, unless and until the Production Manager says so. """
===

class

Producer (PowerDNS)   One enterprise-wide
The Producer manages our DNS to
Optional/Not Currently Implemented
