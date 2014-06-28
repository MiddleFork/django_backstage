from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from mezzanine.core.views import direct_to_template
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns("",
    ("^admin/", include(admin.site.urls)),
    # HOMEPAGE AS STATIC TEMPLATE
    url("^$", direct_to_template, {"template": "index.html"}, name="home"),
    # HOMEPAGE AS AN EDITABLE PAGE IN THE PAGE TREE
    #url("^$", "mezzanine.pages.views.page", {"slug": "/"}, name="home"),
)
# NECESSARY for the DEBUG TOOLBAR pre 1.7
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )

# NECESSARY for staticfiles to appear in development server
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()

#Mezzanine if used as a catch-all must be the final include
urlpatterns += patterns("",
                        ("^", include("mezzanine.urls")),
                        )
