from django.db import models


class Post(models.Model):
    """Post Model
    Fields:
        organizer (ForeignKey): the user that made the event
        game (ForeignKey): the game associated with the event
        date (DateField): The date of the event
        time (TimeFIeld): The time of the event
        description (TextField): The text description of the event
        attendees (ManyToManyField): The gamers attending the event
    """
    user = models.ForeignKey("RareUser", on_delete=models.CASCADE)
    category = models.ForeignKey("Category", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=250)
    content = models.TextField()
    approved = models.BooleanField()