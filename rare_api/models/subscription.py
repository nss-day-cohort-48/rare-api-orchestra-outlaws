from django.db import models
from django.contrib.auth.models import User


class Subscription(models.Model):
    follower = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    author = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    created_on = models.DateField()
    ended_on = models.DateField(default=None, blank=True, null=True)

    def __str__(self):
        return self.follower.user.username + " is following " + self.author.user.username
