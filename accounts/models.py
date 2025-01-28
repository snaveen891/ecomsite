from django.db import models
from django.conf import settings

import hashlib
def user_directory_path(instance, filename):
    u_hash = hashlib.sha256(str(instance.user.id).encode()).hexdigest()[:10]
    return f"users/{u_hash}/{filename}"


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to=user_directory_path, blank=True)
    
    def __str__(self):
        return f'Profile for user {self.user.username}'
    

















