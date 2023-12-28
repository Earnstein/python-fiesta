from django.db import models

class StreamPlatform(models.Model):
    name = models.CharField(max_length=20)
    about = models.CharField(max_length=200)
    website = models.URLField(max_length=100)
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Watchlist(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    platform = models.ForeignKey(StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")
    created = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
