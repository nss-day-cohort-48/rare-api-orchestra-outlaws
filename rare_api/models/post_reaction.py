from django.db import models


class PostReaction(models.Model):
    """PostReactions Model
    Fields:
        user (ForeignKey): the user that made the post reaction
        post (ForeignKey): the post the reaction is for
        reaction (DateField): the reaction given to the post
    """
    rare_user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    reaction = models.ForeignKey("Reaction", on_delete=models.CASCADE)

    def __str__(self):
        return self.description