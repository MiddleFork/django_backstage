from .db_settings import DATABASES
from .common_settings import *
#Import all venue-specific settings
from .venue_settings import *

for app in VENUE_APPS:
    app in INSTALLED_APPS or INSTALLED_APPS.append(app)
