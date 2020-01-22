from django.db import models
from django.contrib.auth.models import User
from datetime import datetime  
from datetime import timedelta 
from django.utils import timezone
# Create your models here.



class EmailVerification(models.Model):

    user_id  = models.ForeignKey(User,on_delete=models.CASCADE)
    token  = models.TextField()
    created_date = models.DateTimeField() 
    status = models.BooleanField(default=False)


    def save(self, *args, **kwargs): 
        self.created_date =  datetime.now(tz=timezone.utc)
        super(EmailVerification, self).save(*args, **kwargs)


class Client(models.Model):

    email = models.EmailField(max_length=254)
    domain  =  models.URLField(max_length=200)
    created_date =  models.DateTimeField()

    def save(self, *args, **kwargs): 
        self.created_date =  datetime.now(tz=timezone.utc)
        super(Client, self).save(*args, **kwargs)



class Otp(models.Model):

    user_id =   models.ForeignKey(User,on_delete=models.CASCADE)
    token  =   models.IntegerField()
    created_date =  models.DateTimeField()
    number_attempt =  models.IntegerField()
    block_status  =  models.BooleanField(default=False)
    created_date =  models.DateTimeField()
    blocked_time  = models.DateTimeField()

    def save(self, *args, **kwargs): 
        self.created_date =  datetime.now(tz=timezone.utc)
        super(Otp, self).save(*args, **kwargs)






    




