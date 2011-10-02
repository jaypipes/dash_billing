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
import json
import pprint
import urllib

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
from models import AccountRecord
from models import EventLog
from django_openstack.decorators import enforce_admin_access
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

import openstack.compute.servers
import openstackx.api.exceptions as api_exceptions

LOG = logging.getLogger('django_openstack.dash')

class CreateAccountRecord(forms.SelfHandlingForm):
    tenant_id = forms.CharField(max_length="100", label="Tenant ID")
    amount = forms.DecimalField(label="Amount")
    memo = forms.CharField(max_length="300", label="Memo")

    def handle(self, request, data):
        accountRecord = AccountRecord(tenant_id=data['tenant_id'],amount=int(data['amount']),memo=data['memo'])
        accountRecord.save()
        msg = '%s was successfully added to .' % data['tenant_id']
        LOG.info(msg)
        messages.success(request, msg)
        return shortcuts.redirect('syspanel_billing')


class DeleteAccountRecord(forms.SelfHandlingForm):
    id = forms.CharField(required=True)

    def handle(self, request, data):
        try:
            id = data['id']
            print "id %s" % id
            LOG.info('Deleting account with id "%s"' % id)
            accountRecord = AccountRecord.objects.get(id=id)
            print "delete %r" % accountRecord
            accountRecord.delete()

            messages.info(request, 'Successfully deleted record: %s' %
                          id)
        except api_exceptions.ApiException, e:
            messages.error(request, 'Unable to delete recode: %s' %
                                     e.message)
        return shortcuts.redirect(request.build_absolute_uri())


@login_required
@enforce_admin_access
def index(request):
    for f in (DeleteAccountRecord,):
        _, handled = f.maybe_handle(request)
        if handled:
            return handled
    delete_form = DeleteAccountRecord()

    account_record_list = AccountRecord.objects.order_by('time').reverse()

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

    return shortcuts.render_to_response('syspanel_billing.html', 
    {'account_record_list':records, 'delete_form': delete_form}, context_instance=template.RequestContext(request))

def eventlog(request):
    tenant_id = request.session['tenant_id']
    eventlog_list = EventLog.objects.order_by('created').reverse()

    request_id = request.GET.get('request_id')
    if request_id:
        eventlog_list = eventlog_list.filter(request_id=request_id)

    priority = request.GET.get('priority')
    if priority:
        eventlog_list = eventlog_list.filter(priority=priority)

    paginator = Paginator(eventlog_list,100)
    page = request.GET.get('page')
    try:
        records = paginator.page(page)
    except TypeError:
        # If page is not an integer, deliver first page.
        records = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        records = paginator.page(paginator.num_pages)


    for obj in records.object_list:
        obj.message = pprint.pformat(json.loads(obj.message))

    template_file = 'syspanel_eventlog.html'
    if request.GET.get('refresh',False):
        template_file = '_eventlog.html'

    query = '&'.join(['%s=%s' % (urllib.quote(key),urllib.quote(value[0]))
        for key,value in request.GET.lists() if key != 'page' ])
    return shortcuts.render_to_response(template_file,
    {'eventlog_list':records,'query':query}, context_instance=template.RequestContext(request))

@login_required
@enforce_admin_access
def create(request):
    form, handled = CreateAccountRecord.maybe_handle(request)
    if handled:
        return handled
    return shortcuts.render_to_response('syspanel_create_account.html',{
        'form': form,
    }, context_instance = template.RequestContext(request))

