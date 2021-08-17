from django.db import models


class Post(models.Model):
    """Post Model
    """
    rare_user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=250)
    content = models.TextField()
    approved = models.BooleanField()