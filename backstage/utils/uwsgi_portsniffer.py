import os
from subprocess import Popen, PIPE
import time
"""uwsgi_portsniffer.py
"""

def get_uwsgi_port(inst):
        """Get the uwsgi port using lsof.  Requires that lsof and fuser be suid root"""
        start_port = None
        timeout = 10
        nap = 1
        starttime = time.time()
        elapsed = 0
        valid = False
        uwsgi_ip = None
        uwsgi_port = None
        while not valid and elapsed < timeout:
            try:
                fullport = port_from_lsof(inst)
                new_ip, new_port = fullport.split(':')
                if new_port != start_port:
                    uwsgi_ip = new_ip
                    uwsgi_port = new_port
                    print 'OK %s:%s' % (uwsgi_ip, uwsgi_port)
                    valid = True
            except:
                pass
            if not valid:
                time.sleep(nap)
                elapsed = time.time() - starttime
        return uwsgi_ip, uwsgi_port



def port_from_lsof(inst):
    try:
        pidfile = inst.uwsgi_config['pidfile']
    except:
        print 'could not determine the socket PID file'
        raise
    try:
        with open(pidfile, 'r') as f:
            pid = f.readline().strip()
    except IOError:
        err = 'Error getting PID from %s' % (pidfile)
        print err
        return None
    try:
        p1 = Popen(['lsof', '-a', '-p%s' % (pid), '-i4'], stdout=PIPE)
        p2 = Popen(["grep", "LISTEN"], stdin=p1.stdout, stdout=PIPE)
        output = p2.communicate()[0]
        port = output.split()[8]
        #print 'OK: %s' % (port)
        return port
    except:
        return None


def portsniffer(log_file):
    if not os.path.exists(log_file):
        print 'Log file not found: %s' % log_file
        return None
    try:
        fo = open(log_file, 'r')
    except:
        print 'Could not open log file: %s' % log_file
        return None, None

    found_port = None
    found_ip = None
    try:
        for l in fo.readlines():
            if 'bound to TCP address' in l:
                before0, after0 = l.split('address')

                before1, after1 = after0.split('(port')
                before1 = before1.strip()
                ip, port = before1.split(':')
                found_ip = ip
                found_port = port
        fo.close()
    except Exception, e:
        print 'Error scanning log file: %s' % log_file
        print e
        return None, None
    return found_ip, found_port
