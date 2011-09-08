"""
URLs for Openstack Dashboard Iframer Module.
"""

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('dash_billing.syspanel.views',
    url(r'^syspanel/billing/$', 'index', name='syspanel_billing'),
    url(r'^syspanel/billing/create/$', 'create', name='syspanel_billing_create'),
)


