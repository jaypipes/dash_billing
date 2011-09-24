# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
#
# Copyright 2011 Fourth Paradigm Development, Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""
Views for managing Nova instances.
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

from django_openstack import api
from django_openstack import forms
from django_openstack import utils
from django.db.models.aggregates import Sum

from dash_billing.syspanel.models import  AccountRecord

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import openstack.compute.servers
import openstackx.api.exceptions as api_exceptions


LOG = logging.getLogger('django_openstack.dash')

@login_required
def index(request):
    tenant_id = request.session['tenant_id']
    print '%r' % tenant_id
    account_record_list = AccountRecord.objects.filter(tenant_id=tenant_id)
    paginator = Paginator(account_record_list,30)
    page = request.GET.get('page')
    try:
        records = paginator.page(page)
    except TypeError:
        # If page is not an integer, deliver first page.
        records = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        records = paginator.page(paginator.num_pages)
    balance = AccountRecord.objects.filter(tenant_id=tenant_id).aggregate(Sum('amount'))
    return shortcuts.render_to_response('dash_billing.html', 
    {'account_record_list':records,'balance':balance['amount__sum']}, context_instance=template.RequestContext(request))


