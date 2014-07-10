#act_settings.py
SITE_ID = 1
SITE_DB = 'None'
#very weird bug causes nginx to throw 400 errors if debug = False
#so do not do that!
DEBUG = True
TEMPLATE_DEBUG = True


ACT_APPS = [] # APPS to include in INSTALLED_APPS

WWW_DEFAULT_TLD = '.com'
WWW_DEFAULT_HOSTS = ['', 'www']
WWW_SERVER_NAME_LIST = []
# List of web servers this act services
#if empty it will be generated from WWW_DEFAULT_TLD and WWW_DEFAULT_HOSTS