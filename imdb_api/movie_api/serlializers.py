from rest_framework import serializers
from .models import Watchlist, StreamPlatform, Review


class ReviewSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class WatchListSerialiser(serializers.ModelSerializer):
    reviews = ReviewSerialiser(many=True, read_only=True)
    class Meta:
        model = Watchlist
        fields = '__all__'
        depth = 1

class StreamPlatformSerialiser(serializers.HyperlinkedModelSerializer):
    watchlist = WatchListSerialiser(many=True, read_only=True)
    class Meta:
        model = StreamPlatform
        exclude = ["created"]

        