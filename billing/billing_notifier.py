# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
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

import json
import nova
import nova.context
from nova.exception import Error
from nova import flags
from nova import rpc
import logging
import logging.handlers
from nova import log as LOG
from nova.notifier import api

FLAGS = flags.FLAGS
flags.DEFINE_string('notification_topic', 'notification',
                    'RabbitMQ topic used for Nova notifications')

def api_decorator(name, fn):
    """ decorator for notify which is used from utils.monkey_patch()

        :param name: name of the function
        :param function: - object of the function
        :returns: function -- decorated function

    """
    def wrapped_func(*args, **kwarg):
        body = {}
        body['args'] = []
        body['kwarg'] = {}
        original_args = args
        if len(args) >= 2:
            #body['self'] = args[0]
            body['context'] = args[1]
            args = args[3:]
        for arg in args[3:]:
            body['args'].append(arg)
        for key in kwarg:
            body['kwarg'][key] = kwarg[key]
        api.notify(FLAGS.default_publisher_id,
                            name,
                            FLAGS.default_notification_level,
                            body)
        ret = None
        try:
            ret = fn(*original_args, **kwarg)
        except Error as e:
            body['error'] = "%s" % e
            api.notify(FLAGS.default_publisher_id,
                            name,
                            'ERROR',
                            body)
            raise e
        return ret
    return wrapped_func

def emit(self, record):
    api.notify('nova.error.publisher', 'error_notification',
         api.ERROR, dict(error=self.format(record).split('\n')))

def notify(message):
    """Notifies the recipient of the desired event given the model.
    Log notifications using nova's default logging system"""
    context = nova.context.get_admin_context()
    message['method'] = 'notify'
    priority = message.get('priority',
                           FLAGS.default_notification_level)
    priority = priority.lower()
    rpc.cast(context, FLAGS.notification_topic, {'method':'notify','args':{'message':message}})

#Patching Emit function
nova.log.PublishErrorsHandler.emit = emit
