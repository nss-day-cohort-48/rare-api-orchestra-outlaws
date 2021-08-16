from django.db import models


class PostReactions(models.Model):
    """PostReactions Model
    Fields:
        user (ForeignKey): the user that made the post reaction
        post (ForeignKey): the post the reaction is for
        reaction (DateField): the reaction given to the post
    """
    user = models.ForeignKey("", on_delete=models.CASCADE)
    post = models.ForeignKey("", on_delete=models.CASCADE)
    reaction = models.ForeignKey("", on_delete=models.CASCADE)

    def __str__(self):
        return self.description