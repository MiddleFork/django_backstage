The Backstage Producer

The Backstage Producer works on the production server level.

The primary roles of the producer are:

* setup the production server environment for backstage
    - create the backstage user
    - give the backstage user/group write access to the following:
        + /etc/ngnix/sites- [available, enabled]
        + /etc/uwsgi-emperor/vassals
        + /var/log/uwsgi
        + /var/log/nginx

    - give the backstage user permission to gracefully reload nginx

    - setup the postgresql environment for backstage
        + create the backstage postgres user
        + create the backstage database w owner backstage

    - maintain virtual environment configuration files

    - deploy virtual environments, venues, etc.