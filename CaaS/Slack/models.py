from django.db import models
from Connector.models import SSCConnector

class Slack(models.Model):
    source_id = models.ForeignKey(SSCConnector, on_delete=models.CASCADE,null=True, blank=True)
    auth_token = models.CharField(max_length=512)
    api_app_id = models.CharField(max_length=512)
    user_id  = models.CharField(max_length=1024, blank=True, null=True)
    default_channel = models.CharField(max_length=1024, blank=True, null=True)
    flag = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    config  = models.CharField(max_length=1024, blank=True, null=True)

class SlackRequest(models.Model):
    installation = models.ForeignKey(Slack, on_delete=models.CASCADE,null=True, blank=True)
    message = models.TextField()
    channel = models.CharField(max_length=1024)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.message

