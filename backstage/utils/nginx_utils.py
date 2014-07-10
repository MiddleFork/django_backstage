__author__ = 'walker'
"""
nginx.py
backstage tools for building and deploying nginx servers
"""
import os
import sys
import backstage
from backstage.shortcuts import Act, Venue

confdir = os.path.join(os.path.dirname(os.path.abspath(backstage.__file__)), 'conf')
confsrc = os.path.join(confdir, 'nginx.conf.src')

def build_nginx_conf(instance):
    outdir = outpath(instance)
    outfile = instance.longname + '.conf'
    of = open(os.path.join(outdir, outfile), 'w')
    with open(confsrc, 'r') as infile:
        confdata = infile.read()

    # data to substitute into the content
    longname = instance.longname
    server_list_string = instance.settings.WWW_SERVER_NAMES
    listen_addr = instance.settings.NGINX_LISTEN_ADDR
    if isinstance(instance, Act):
        venue_path = instance.venue.venue_home
    elif isinstance(instance, Venue):
        venue_path = instance.venue_home
    confdata = confdata.format(name=instance.name, longname=longname, venue_path=venue_path, server_list_string=server_list_string, listen_addr=listen_addr)
    of.write(confdata)
    of.close()
    return

def outpath(instance):
    op = ''
    if isinstance(instance, Act):
        op = instance.venue.venue_home
    elif isinstance(instance, Venue):
        op = instance.venue_home
    else:
        print 'instance error'
        raise
    op += '/.LIVE'
    return op