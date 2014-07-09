table = 'uwsgi_vassals'
config = 'dummy text'
uid = 'backstage'
gid = 'adm'

uwsgi_defaults = {
    'master': 'True',
    'processes': '8',
    'http-socket': '127.0.0.1:0',
    'plugins': 'python',
    'harikiri': '20',
    'log-maxsize': '100000',
    'max-requests': '1000',
    'vacuum': 'true',
    'disable-logging': 'true',
    'uid': 'backstage',
    'gid': 'adm',
    'logfile-chown': 'true',
    'logfile-chmod': '666',
    }

venue_seeds = {
    'home': '{VENUE_HOME}/venv',
    'virtualenv': '{VENUE_HOME}/venv',
    'pythonpath': '{VENUE_ROOT}',
    'chdir': '{VENUE_ROOT}',
    'module': '{VENUE_NAME}.wsgi:application',
    'pidfile': '{VENUE_HOME}/.LIVE/uwsgi-backstage-{VENUE_NAME}.pid',
    'socket': '{VENUE_HOME}/.LIVE/uwsgi-backstage-{VENUE_NAME}.sock',
    'daemonize': '/var/log/uwsgi/uwsgi-backstage-{VENUE_NAME}.log',
}

act_seeds = {
    'home': '{VENUE_HOME}/venv',
    'virtualenv': '{VENUE_HOME}/venv',
    'chdir': '{VENUE_HOME}/acts',
    'pythonpath': '{VENUE_HOME}/acts',
    'module': '{ACT_NAME}.wsgi:application',
    'pidfile': '{VENUE_HOME}/.LIVE/uwsgi-backstage-{VENUE_NAME}-{ACT_NAME}.pid',
    'socket': '{VENUE_HOME}/.LIVE/uwsgi-backstage-{VENUE_NAME}-{ACT_NAME}.sock',
    'daemonize': '/var/log/uwsgi/uwsgi-backstage-{VENUE_NAME}-{ACT_NAME}.log',
}


def format_act_options(act):
    opts = {}
    for k, v in act_seeds.iteritems():
        opts[k] = v.format(VENUE_HOME=act.venue.venue_home, VENUE_NAME=act.venue.name, ACT_NAME=act.name)
    return opts


def build_uwsgi(obj, objtype):
    """
    build a string formatted like a uwsgi.ini file
    @return:
    """
    uwsgi_config = {}
    for k, v in uwsgi_defaults.iteritems():
        uwsgi_config[k] = v


    options = {
        'act': format_act_options,
        'venue': format_venue_options,
        }

    local_options = options[objtype](obj)
    for k, v in local_options.iteritems():
        uwsgi_config[k] = v

    uwsgi_ini = '[uwsgi]\n'
    for k, v in uwsgi_config.iteritems():
        uwsgi_ini += '%s = %s\n' % (k, v)
    return uwsgi_config, uwsgi_ini


def format_venue_options(venue):
    opts = {}
    for k, v in venue_seeds.iteritems():
        opts[k] = v.format(VENUE_HOME=venue.venue_home, VENUE_NAME=venue.venue_name, VENUE_ROOT=venue.venue_root)
    return opts

