from django.db import models

class Tag(models.Model):
    """Tag Model"""
    label = models.CharField(max_length=10)