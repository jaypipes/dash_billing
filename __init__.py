from django.dispatch import *

from django_openstack.signals import dash_modules_ping
from django_openstack.signals import dash_modules_urls

import urls


@receiver(dash_modules_ping, dispatch_uid="fooooo")
def send_sidebar_nav(sender, **kwargs):
    return {'title': MODULE_TITLE, 'links': LINKS, 'type': MODULE_TYPE}
    

@receiver(dash_modules_urls, dispatch_uid="fooooo")
def set_module_urls(sender, **kwargs):
    return urls


## Items above are required to allow your module to work.

## Items below are used to define what is placed in the sidebar navigation.


MODULE_TITLE = "Nixon"
MODULE_TYPE = "syspanel" # use 'dash' for user dashboard
LINKS = [
    {'url':'/syspanel/nixon/google', 'text':'Google', 'active_text': 'google'},
    # {'url':'http://google.com', 'text':'ffff'},
]
