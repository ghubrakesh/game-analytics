from django.db import models


class GameData(models.Model):
    app_id = models.IntegerField()
    name = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    required_age = models.IntegerField(null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    dlc_count = models.IntegerField(null=True, blank=True)
    about_the_game = models.TextField(null=True, blank=True)
    supported_languages = models.TextField(null=True, blank=True)
    windows = models.BooleanField(default=False)
    mac = models.BooleanField(default=False)
    linux = models.BooleanField(default=False)
    positive = models.IntegerField(null=True, blank=True)
    negative = models.IntegerField(null=True, blank=True)
    score_rank = models.IntegerField(null=True, blank=True)
    developers = models.CharField(max_length=255, null=True, blank=True)
    publishers = models.CharField(max_length=255, null=True, blank=True)
    categories = models.TextField(null=True, blank=True)
    genres = models.TextField(null=True, blank=True)
    tags = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
