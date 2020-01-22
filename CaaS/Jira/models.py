from django.db import models
from django.db.models import Model 
from django.utils import timezone
from django.contrib.auth.models import User



# Create your models here.
class Jira(models.Model):
	app_url = models.URLField(max_length=200, blank=False, null=False) 
	email_id = models.EmailField(blank=False, null=False)
	api_key = models.TextField()
	project_key = models.TextField(blank=False, null=False)
	jira_config = models.TextField(blank=True, null=True)
	flag = models.BooleanField(default=False)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)

	