from django.db import models

class AccountRecord(models.Model):
    tenant_id = models.CharField(max_length=200)
    amount = models.IntegerField()
    memo = models.TextField()
    time = models.DateTimeField(auto_now_add=True)
