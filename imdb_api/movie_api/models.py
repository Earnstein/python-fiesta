from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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

class Review(models.Model):
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.rating)