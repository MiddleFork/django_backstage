# attach all the settings variables to templates
# doesn't seem to work with keyword 'settings' hence 'csettings' is used
def settings_constants(request):
    from django.conf import settings
    return {'csettings':settings,}
