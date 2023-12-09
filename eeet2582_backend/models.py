from django.db import models

class UserProfile(models.Model):
    # Add your additional fields here
    # For example:
    provider = models.TextField(max_length=500, blank=True)
    provider_id = models.TextField(max_length=500, blank=True)
    name = models.TextField(max_length=500, blank=True)
    email = models.TextField(max_length=500, blank=True)
    picture = models.TextField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)