from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

class customuser(AbstractUser):
    is_seller = models.BooleanField(default=False)




