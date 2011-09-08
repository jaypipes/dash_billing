"""
URLs for Openstack Dashboard Iframer Module.
"""

from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('dash_billing.dash.views',
    url(r'^dash/dash_billing/billing/$', 'index', name='dash_billing'),
)


