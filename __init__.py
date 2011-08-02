from django.dispatch import *

from django_openstack.signals import dash_apps_ping
from django_openstack.signals import dash_apps_urls

import urls


@receiver(dash_apps_ping, dispatch_uid="fooooo")
def send_sidebar_nav(sender, **kwargs):
    return {'title': MODULE_TITLE, 'links': LINKS, 'type': MODULE_TYPE}
    

@receiver(dash_apps_urls, dispatch_uid="fooooo")
def set_module_urls(sender, **kwargs):
    return urls


## Items above are required to allow your module to work.

## Items below are used to define what is placed in the sidebar navigation.


MODULE_TITLE = "Monitoring"
MODULE_TYPE = "syspanel" # use 'dash' for user dashboard
LINKS = [
    {'url':'/syspanel/nixon/munin', 'text':'Munin', 'active_text': 'munin'},
    # {'url':'http://google.com', 'text':'ffff'},
]
