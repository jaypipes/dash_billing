from django.db import models

class AccountRecord(models.Model):
    tenant_id = models.CharField(max_length=200)
    amount = models.IntegerField()
    memo = models.TextField()
    time = models.DateTimeField(auto_now_add=True)


class EventLog(models.Model):
    tenant_id = models.CharField(max_length=200,blank=True)
    event_type =  models.CharField(max_length=200,blank=True)
    priority =  models.CharField(max_length=200,blank=True)
    publisher_id =  models.CharField(max_length=200,blank=True)
    user_id =  models.CharField(max_length=200,blank=True)
    request_id = models.CharField(max_length=36,blank=True)
    message_id = models.CharField(max_length=36,blank=True)
    message = models.TextField()
    status = models.CharField(max_length=200,blank=True)
    created = models.DateTimeField(auto_now_add=True)
