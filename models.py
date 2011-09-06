from django.db import models
from django.contrib.auth.models import User

class AuthToken(models.Model):
	user = models.OneToOneField(User,unique=True)
	download_ticket = models.CharField(max_length=32)
	session_id = models.CharField(max_length=32)
	latest_version= models.CharField(max_length=32)
