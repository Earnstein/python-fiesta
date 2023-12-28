from rest_framework import serializers
from .models import Watchlist, StreamPlatform

class WatchListSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = '__all__'

class StreamPlatformSerialiser(serializers.ModelSerializer):
    class Meta:
        model = StreamPlatform
        fields = '__all__'