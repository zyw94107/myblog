from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    nick_name = models.CharField(max_length=100,blank=True)
    class Meta(AbstractUser.Meta):
        pass