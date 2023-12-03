from rest_framework import serializers
from .models import Movie

class MovieSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'active']



# class MovieSerialiser(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name  = serializers.CharField()
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self,validated_data):
#         """
#         Create and return a new `Movie` instance, given the validated data.
#         """
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Movie` instance, given the validated data.
#         """
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance