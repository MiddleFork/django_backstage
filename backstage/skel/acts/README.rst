In Django Backstage, we borrow the noun 'Act' in its usage as 'a musical group', similar terms being 'group', 'band' 'ensemble', etc.

A Django Backstage Act is essentially an Django App.

Thus, an Act like a regular django app is deployable as a uWSGI application.  But

An Act can be seen as a deployable django uWSGI application that can (but need not be) bound to a
web site.

In other words, an Act can be running all day long on but unless a public facing web server like
apache or nginx is deploying the Act on a (django-terminology) 'Site' nobody but the developer
will know or care.

Instead, an Act needs a Gig at a specific Venue in order to be publicized to the wide web.
