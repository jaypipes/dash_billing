"""
URLs for Openstack Dashboard Iframer Module.
"""


from django.conf.urls.defaults import *
from django.conf import settings


SYSPANEL = r'^syspanel/nixon/%s$'
DASH = r'^dash/nixon/%s$'


urlpatterns = patterns('nixon.views',
    url(SYSPANEL % 'google', 'google', name='os_dash_nixon_google'),
)
