from django.db import models
from django.contrib.auth.models import User
from jsonfield import JSONField
# Create your models here.


class SSCConnector(models.Model):
    interval = models.IntegerField(null=False)
    api_url= models.URLField(max_length=255, blank=False, null=False)
    api_token = models.TextField(blank=False, null=False)
    overall_score = models.IntegerField()
    factor_score = models.IntegerField()
    issue_level_event = models.IntegerField()
    domain = models.URLField()
    flag = models.BooleanField(default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class TargetApplication(models.Model):
    app_name = models.CharField(max_length=200, blank=False, null=False)
    app_logo = models.ImageField(upload_to="static/logos/", blank=False, null=False)
    required_fields = JSONField()


  
