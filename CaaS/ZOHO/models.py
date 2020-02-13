from django.db import models

from django.db import models
from Connector.models import SSCConnector
# Create your models here.
from datetime import datetime  
from datetime import timedelta 
from django.utils import timezone



class  Zohomodel(models.Model):
    source_id = models.ForeignKey(SSCConnector, on_delete=models.CASCADE,null=True, blank=True)
    token   = models.CharField(max_length=512)
    contact_id  = models.CharField(max_length=512)
    department_id= models.CharField(max_length=512)
    config =  models.CharField(max_length=512)
    flag =  flag =  models.BooleanField(default=False)
    created_date =  models.DateTimeField()


    def save(self, *args, **kwargs): 
        self.created_date =  datetime.now(tz=timezone.utc)
        super(Zohomodel, self).save(*args, **kwargs)



