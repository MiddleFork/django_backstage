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


class Venue:
    In Backstage, a Venue is analogous to a plain vanilla Django project.  Just as a project may have a number of Apps, a Venue may have a number of Acts.
    The Venue is also the top-level of a virtual environment.  Think: VENue = Virtual ENvironment to help remember.

class Act:
    An Act is essentially a runnable Django application.   (Runnable, not necessarily Running.)  The analogy is a musical Act (performer, ensemble, group, etc.)  Miles Davis sometimes had the reputation of being reclusive. Davis may have gone periods between performances, but remained a musical Act all the while.   It's the existence, not their performance (in the case of musicians) that define them as Acts; likewise it is the existence of your app, not the fact that it is running, that defines it as an Act."""

So, what does backstage do?

* Backstage allows you to create and launch Django projects and apps extremely quickly.
* It handles building and deploying the python virtual environment.
* Backstage integrates with uWSGI and allows you to stop and restart Acts on the fly without restarting the web server.

Getting Started:

::

    pip install django_backstage
    from backstage.shortcuts import new_venue, new_act\n
    venue = new_venue('MyVenue', '/tmp') # create a new venue named 'MyVenue' and place it in the /tmp folder.
    # this will build the Virtual Environment for the Venue
    act = new_act(venue,'MyAct') # creates a new Act at MyVenue/acts/MyAct and immediately launches it as a uWSGI application, using the Venue's virtual environment.
    act.get_uwsgi_port() # return the port the Act is bound to.
    # you can now point your browser to http://localhost:PORT to view your running Act (no need to ever run manage.py runserver ever again!)
    act.stop() # stop a running Act
    act.start() # start an Act``

Those are the basics for now.
