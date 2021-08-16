from django.db import models

INPUT_MAX_LENGTH = 255

class Reaction(models.Model):
    label = models.CharField(max_length=INPUT_MAX_LENGTH)
    image_url = models.CharField(max_length=INPUT_MAX_LENGTH)