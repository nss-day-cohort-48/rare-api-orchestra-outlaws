
from rare_api.models.reaction import Reaction
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

    @property
    def reaction_counter(self):
        reactions = Reaction.objects.filter(post=self).values('id', 'label', 'image_url')
        reaction_counter = {}
        for reaction in reactions:
            if reaction['id'] in reaction_counter:
                reaction_counter[reaction['id']]['count'] += 1
            else:
                reaction_counter[reaction['id']] = {'count': 1, 'image_url': reaction['image_url']}
        return reaction_counter