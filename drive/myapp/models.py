from django.db import models
from django.contrib.auth.models import User

class User(models.Model):
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)

#python manage.py makemigrations
#python manage.py migrate 