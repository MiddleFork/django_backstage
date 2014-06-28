######################
# MEZZANINE SETTINGS #
######################
MEZZANINE_AUTHENTICATION_BACKENDS = ["mezzanine.core.auth_backends.MezzanineBackend",]

################
# APPLICATIONS #
################
MEZZANINE_INSTALLED_APPS = [
    "mezzanine.boot",
    "mezzanine.conf",
    "mezzanine.core",
    "mezzanine.generic",
    "mezzanine.blog",
    "mezzanine.forms",
    "mezzanine.pages",
    "mezzanine.galleries",
    "mezzanine.twitter",
    "mezzanine.template",
    #"mezzanine.accounts",
    #"mezzanine.mobile",
]

MEZZANINE_TEMPLATE_CONTEXT_PROCESSORS = [
    "mezzanine.conf.context_processors.settings",
    "mezzanine.pages.context_processors.page",
]

MEZZANINE_MIDDLEWARE_CLASSES_PREPEND = ["mezzanine.core.middleware.UpdateCacheMiddleware", ]

MEZZANINE_MIDDLEWARE_CLASSES_APPEND = [
    "mezzanine.core.request.CurrentRequestMiddleware",
    "mezzanine.core.middleware.TemplateForDeviceMiddleware",
    "mezzanine.core.middleware.TemplateForHostMiddleware",
    "mezzanine.core.middleware.AdminLoginInterfaceSelectorMiddleware",
    "mezzanine.core.middleware.SitePermissionMiddleware",
    # Uncomment the following if using any of the SSL settings:
    # "mezzanine.core.middleware.SSLRedirectMiddleware",
    "mezzanine.pages.middleware.PageMiddleware",
    "mezzanine.core.middleware.FetchFromCacheMiddleware",
]


# Store these package names here as they may change in the future since
# at the moment we are using custom forks of them.
PACKAGE_NAME_FILEBROWSER = "filebrowser_safe"
PACKAGE_NAME_GRAPPELLI = "grappelli_safe"

#sjw not sure where this is set in the off-the-shelf mez.
TESTING = False


MEZZANINE_TEMPLATE_DIRS = [
    'galleries/templates',
    'generic/templates',
    'accounts/templates',
    'mobile/templates',
    'blog/templates',
    'core/templates',
    'pages/templates',
    'conf/templates',
    'forms/templates',
    'twitter/templates',
    ]


NEVERCACHE_KEY = "57bd470d-598c-4d72-b8bb-a7be02f534fca1c6b3d0-a814-4514-b3a9-d7fad4a3d8b17041ba11-aaf7-4b1f-b6dd-b222b7191382"


