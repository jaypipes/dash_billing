# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright (c) 2010 Openstack, LLC.
# Copyright 2010 United States Government as represented by the
# Administrator of the National Aeronautics and Space Administration.
# All Rights Reserved.
# Copyright (c) 2010 NTT
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
Billing Service
"""

import os
import logging
import json
import settings
from datetime import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'dashboard.settings'

from django.core.management import execute_manager
from django_openstack import api
from django_openstack.middleware.keystone import User

from django.db.models.aggregates import Sum

from openstackx.api import exceptions as api_exceptions
from dash_billing.syspanel.models import  AccountRecord

from nova import db
from nova import flags
from nova import log as logging
from nova import manager
from nova import rpc
from nova import utils
from nova.compute import instance_types
from nova.scheduler import zone_manager

LOG = logging.getLogger('django_openstack.cron')

#TODO fix this later(nati)
TENANT = '1'
USER = 'admin'
PASSWORD = 'secrete'

class FakeRequest:
    def __init__(self,user):
        self.user = user

LOG = logging.getLogger('billing.manager')
FLAGS = flags.FLAGS

class PriceList:
    CREATE_INSTANCE = -100
    ACTIVE_INSTANCE = -1

class BillingManager(manager.Manager):
    def __init__(self, *args, **kwargs):
        self.token = api.token_create(None, TENANT, USER, PASSWORD)
        self.user = User(self.token.id,
                USER,
                TENANT,
                True,
                self.token.serviceCatalog
        )
        self.request = FakeRequest(self.user)

    def periodic_tasks(self, context=None):
        self._add_record_for_active_instance()
        self._check_tenant_bill()

    def _add_record_for_active_instance(self):
        now =  datetime.now()
        instances = []
        try:
            instances = api.admin_server_list(self.request)
        except Exception as e:
            LOG.error('Unspecified error in instance index', exc_info=True)
            messages.error(request, 'Unable to get instance list: %s' % e.message)
        for instance in instances:
            if instance.status == 'ACTIVE':
                self._add_record(instance.attrs.tenant_id, PriceList.ACTIVE_INSTANCE, 'instance %s is running at %s' % (instance.id,now))

    def _check_tenant_bill(self):
        tenants = api.tenant_list(self.request)
        #TODO (nati) This code is very slow. FIX this later 
        for tenant in tenants:
            print 'tenant %s %s' % (tenant.id,tenant.description)
            print '%r' % dir(tenant)
            description = tenant.description if tenant.description else '   '
            balance = AccountRecord.objects.filter(tenant_id=tenant.id).aggregate(Sum('amount'))['amount__sum']
            if balance > 0:
                print 'OK tenant.id %s %s' % (tenant.id,balance)
                api.tenant_update(self.request,tenant.id,description,True)
            else:
                print 'NG tenant.id %s %s' % (tenant.id,balance)
                api.tenant_update(self.request,tenant.id,description,False)

    def _add_record(self, tenant_id, amount, memo):
        accountRecord = AccountRecord(tenant_id=tenant_id,amount=amount,memo=memo)
        accountRecord.save()

    def compute_instance_create(self, message):
        self._add_record(message['payload']['project_id'], PriceList.CREATE_INSTANCE, 'create instance')

    def notify(self, message, context=None):
        event_type = message['event_type'].replace('.','_')
        print event_type
        if hasattr(self,event_type):
            method = getattr(self,event_type)
            method(message)
        LOG.debug(json.dumps(message))
