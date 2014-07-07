import os
"""
linker_file_ini.py
Creates vassals for the uWSGI emperor using the pg_emperor plugin.
defines start, stop, and restart functions.  Upstream classes such as Act
can choose which linker from which to load these (eg file:// vs pg_emperor, etc)
"""
def start(inst):
    """
    Start a backstage instance by *linking* it's INI file
    @param inst: Backstage Instance, such as an Act
    @return:
    """
    if not os.path.exists(inst.uwsgi_file):
        with open(inst.uwsgi_file, 'w') as f:
            f.write(inst.uwsgi_ini)

    if os.path.exists(inst.uwsgi_vassal):
        try:
            a = inst.name
        except NameError:
            a = ''
        print 'Vassal file already exists. Hint: try %s.restart() instead' % a
        return
    os.symlink(inst.uwsgi_file, inst.uwsgi_vassal)
    print 'start request submitted for %s' % inst.name
    #inst.get_uwsgi_port()
    return


def stop(inst):
    """
    Stop a backstage instance by *unlinking* it's INI file
    @param inst: Backstage Instance, such as an Act
    @return:
    """
    if not os.path.exists(inst.uwsgi_vassal):
        print 'vassal %s not running' % inst.name
        return
    try:
        os.unlink(inst.uwsgi_vassal)
        print 'stop request submitted for %s' % inst.name
    except:
        print 'error unlinking vassal'
        return
    inst.uwsgi_port = None
    return


def restart(inst):
    """
    Re-start a backstage instance by *touching* it's INI file
    @param inst: Backstage Instance, such as an Act
    @return:
    """
    try:
        with file(inst.uwsgi_file, 'a'):
            os.utime(inst.uwsgi_file, None)
    except IOError:
        print 'Could not update, permission denied.'
        return
    print 're-start request submitted for %s' % inst.name
    #inst.get_uwsgi_port()
    return