import sys
import os
p = os.path.dirname(os.path.abspath(__file__))  # settings
ACT_HOME, n2 = os.path.split(p)
ACTS_DIR, ACT_NAME = os.path.split(ACT_HOME)
VENUE_PATH = os.path.dirname(ACTS_DIR)
VENUE_ROOT, VENUE_NAME = os.path.split(VENUE_PATH)
INSTRUMENTS_ROOT = os.path.abspath(os.path.join(VENUE_PATH, 'instruments'))

#prepend into sys.path in reverse order of importance. The Act itself should
#automatically already be present first in the list
INSTRUMENTS_ROOT in sys.path or sys.path.insert(1, INSTRUMENTS_ROOT)
VENUE_ROOT in sys.path or sys.path.insert(1, VENUE_ROOT)
VENUE_PATH in sys.path or sys.path.insert(1, VENUE_PATH)
ACTS_DIR in sys.path or sys.path.insert(1, ACTS_DIR)
syspath = sys.path
exec('from %s.settings import *' % VENUE_NAME)

from theme_settings import *

from db_settings import DATABASES
DATABASES['default']['NAME'] = 'backstage_%s_%s' % (VENUE_NAME, ACT_NAME)

from act_settings import *


TEMPLATE_DIRS.insert(0, ACT_NAME + '/templates')
TEMPLATE_DIRS.append('%s/instruments/local/templates' % VENUE_ROOT)
TEMPLATE_DIRS.append('%s/instruments/local/templates/ads' % VENUE_ROOT)

ROOT_URLCONF = '%s.urls' % (ACT_NAME)

for act in ACT_APPS:
    act in INSTALLED_APPS or INSTALLED_APPS.append(act)
INSTALLED_APPS.insert(0, ACT_NAME)

del p,n2
sys.path = syspath