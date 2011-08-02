"""
Views for Openstack Dashboard Iframer Module.
"""

import datetime
import logging

from django import http
from django import shortcuts
from django import template
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _


LOG = logging.getLogger('dashboard.osdash_nixon')


from django_openstack import api
from django_openstack import forms
from django_openstack.dash.views import instances as dash_instances
from openstackx.api import exceptions as api_exceptions

@login_required
def munin(request):
    return shortcuts.render_to_response('nixon_munin.html', {
    }, context_instance=template.RequestContext(request))
