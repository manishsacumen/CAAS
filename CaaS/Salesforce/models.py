from django.db import models
from Connector.models import SSCConnector
# Create your models here.
from datetime import datetime  
from datetime import timedelta 
from django.utils import timezone



class Salesforcemodel(models.Model):
    source_id = models.ForeignKey(SSCConnector, on_delete=models.CASCADE,null=True, blank=True)
    url    = models.CharField(max_length=512)
    username  = models.CharField(max_length=512)
    password = models.CharField(max_length=512)
    client_id = models.CharField(max_length=512)
    client_secret = models.CharField(max_length=512)
    security_token = models.CharField(max_length=512)
    config =  models.CharField(max_length=512)
    flag =  models.BooleanField(default=False)
    created_date =  models.DateTimeField()


    def save(self, *args, **kwargs): 
        self.created_date =  datetime.now(tz=timezone.utc)
        super(Salesforcemodel, self).save(*args, **kwargs)



