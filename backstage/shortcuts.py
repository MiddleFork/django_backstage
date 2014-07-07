"""
backstage shortcuts.py
Shortcut imports for convenience.
"""

# Choose one of the below as the default uwsgi emperor vassal control:
from backstage.utils.uwsgi.linker_file_ini import start, stop, restart
#from backstage.utils.uwsgi.linker_pg_plugin import start, stop, restart


from backstage.act.act import Act
from backstage.venue.venue import Venue

from backstage.venue.venue_utils import  new_venue, venue_from_cwd
from backstage.act.act_utils import  new_act






