from django.db import models

# Create your models here.

class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    

#python manage.py makemigrations
#python manage.py migrate 
#zob humide frere kiya hua hai