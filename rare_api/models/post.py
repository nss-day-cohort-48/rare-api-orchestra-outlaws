from django.db import models
from django.db.models.deletion import CASCADE


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
    tags = models.ManyToManyField("Tag", through="PostTag")
    reactions = models.ManyToManyField("Reaction", through="PostReaction")

    @property
    def isMine(self):
        return self.__isMine

    @isMine.setter
    def isMine(self, value):
        self.__isMine = value
