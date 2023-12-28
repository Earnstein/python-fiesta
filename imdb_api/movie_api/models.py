from django.db import models

class Watchlist(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class StreamPlatform(models.Model):
    name = models.CharField(max_length=20)
    about = models.CharField(max_length=200)
    website = models.URLField(max_length=100)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name
