from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class TodoItem(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    
class Dossier(models.Model):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='sous_dossiers')

    def __str__(self) :
        return self.title
    
class Fichier(models.Model):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey(Dossier, on_delete=models.CASCADE, related_name='fichiers')
    file = models.FileField(upload_to='files/')
    
    def __str__(self) :
        return self.title

class User(models.Model):
  name  = models.CharField(max_length=255, default="Jean")
  email = models.CharField(max_length=255)
  password = models.CharField(max_length=255)


#python manage.py makemigrations
#python manage.py migrate 
#zob humide frere kiya hua hai