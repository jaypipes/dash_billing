from django.dispatch import *

from django_openstack.signals import dash_modules_ping
from django_openstack.signals import dash_modules_urls

import urls


@receiver(dash_modules_ping, dispatch_uid="dash_billing.dash")
def send_sidebar_nav(sender, **kwargs):
    print '%r' % dir(sender)
    return {'title': MODULE_TITLE, 'links': LINKS, 'type': MODULE_TYPE}

@receiver(dash_modules_urls, dispatch_uid="dash_billing.dash")
def set_module_urls(sender, **kwargs):
    return urls


## Items above are required to allow your module to work.

## Items below are used to define what is placed in the sidebar navigation.


MODULE_TITLE = "Billing"
MODULE_TYPE = "dash" # use 'dash' for user dashboard
LINKS = [
    {'url':r'/dash/dash_billing/billing/', 'text':'Billing', 'active_text': 'Billing Pane'},
    # {'url':'http://google.com', 'text':'ffff'},
]
