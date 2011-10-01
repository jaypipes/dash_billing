from django.dispatch import *

from django_openstack.signals import dash_modules_ping
from django_openstack.signals import dash_modules_urls

import urls


@receiver(dash_modules_ping, dispatch_uid="dash_billing.syspanel")
def send_sidebar_nav(sender, **kwargs):
    return {'title': SYSPANEL_MODULE_TITLE, 'links': SYSPANEL_LINKS, 'type': SYSPANEL_MODULE_TYPE}
    

@receiver(dash_modules_urls, dispatch_uid="dash_billing.syspanel")
def set_module_urls(sender, **kwargs):
    return urls


## Items above are required to allow your module to work.

## Items below are used to define what is placed in the sidebar navigation.


SYSPANEL_MODULE_TITLE = "Billing Syspanel"
SYSPANEL_MODULE_TYPE = "syspanel" # use 'dash' for user dashboard
SYSPANEL_LINKS = [
    {'url':'/syspanel/billing/', 'text':'Billing', 'active_text': 'Billing Pane'},
    {'url':'/syspanel/billing/eventlog/', 'text':'EventLog', 'active_text': 'Event Log'},
    # {'url':'http://google.com', 'text':'ffff'},
]
