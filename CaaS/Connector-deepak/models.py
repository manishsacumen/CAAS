from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class SSCConnector(models.Model):
    interval = models.IntegerField(null=False)
    api_url= models.URLField(max_length=255, blank=False, null=False)
    api_token = models.TextField(blank=False, null=False)
    overall_score = models.IntegerField()
    factor_score = models.IntegerField()
    issue_level_event = models.IntegerField()
    domain = models.URLField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)


  
