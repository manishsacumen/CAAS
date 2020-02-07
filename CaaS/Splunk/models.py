from django.db import models
from Connector.models import SSCConnector
# Create your models here.
from datetime import datetime  
from datetime import timedelta 
from django.utils import timezone

class Splunk(models.Model):

    source_id = models.ForeignKey(SSCConnector, on_delete=models.CASCADE,null=True, blank=True)
    api_url = models.CharField(max_length=512)
    hec_token  =  models.CharField(max_length=512)
    flag =  models.BooleanField(default=False)
    config = models.CharField(max_length=512)
    created_date =  models.DateTimeField()


    def save(self, *args, **kwargs): 
        self.created_date =  datetime.now(tz=timezone.utc)
        super(Splunk, self).save(*args, **kwargs)



