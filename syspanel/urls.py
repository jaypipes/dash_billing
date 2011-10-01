"""
URLs for Openstack Dashboard Iframer Module.
"""

import os

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('dash_billing.syspanel.views',
    url(r'^syspanel/billing/$', 'index', name='syspanel_billing'),
    url(r'^syspanel/billing/create/$', 'create', name='syspanel_billing_create'),
    url(r'^syspanel/billing/eventlog/$', 'eventlog', name='syspanel_eventlog'),
)

urlpatterns += patterns(
    '',
    url(r'^billing/static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': os.path.abspath(os.path.join(settings.ROOT_PATH, '..', 'dash_billing/static'))
}),
)


