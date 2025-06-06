from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_2fa_enabled = models.BooleanField(default=False)
    # Add other custom fields here if needed in the future
    # For example:
    # phone_number = models.CharField(max_length=15, blank=True, null=True)
    # profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.username
