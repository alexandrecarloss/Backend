from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    xp = models.IntegerField(default=0)
    nivel = models.IntegerField(default=0)
    is_guest = models.BooleanField(default=False)

    def __str__(self):
        return self.username
