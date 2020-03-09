from django.db import models
from Connector.models import SSCConnector
# Create your models here.
from datetime import datetime  
from datetime import timedelta 
from django.utils import timezone



class  Jitbitmodel(models.Model):
    source_id = models.ForeignKey(SSCConnector, on_delete=models.CASCADE,null=True, blank=True)
    username  =  models.CharField(max_length=512)
    password =  models.CharField(max_length=512)
    categoryId =  models.CharField(max_length=512)
    domain = models.CharField(max_length=512,  null = True)
    config =  models.CharField(max_length=512)
    flag =  flag =  models.BooleanField(default=False)
    created_date =  models.DateTimeField()


    def save(self, *args, **kwargs): 
        self.created_date =  datetime.now(tz=timezone.utc)
        super(Jitbitmodel, self).save(*args, **kwargs)

    


