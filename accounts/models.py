from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)
    email = models.EmailField()
    birthday = models.DateField(null=True, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars', null=True, blank=True)

    def __str__(self):
        return "{}".format(self.user)
