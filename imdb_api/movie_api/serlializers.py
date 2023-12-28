from rest_framework import serializers
from .models import Watchlist, StreamPlatform

class WatchListSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = '__all__'
        depth = 1

class StreamPlatformSerialiser(serializers.ModelSerializer):
    watchlist = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='list_details')
    class Meta:
        model = StreamPlatform
        exclude = ["created"]