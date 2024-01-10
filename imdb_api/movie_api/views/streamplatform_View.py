from ..serlializers import StreamPlatformSerialiser
from rest_framework.response import Response
from ..models import StreamPlatform
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics

class StreamPlatformListAV(generics.ListCreateAPIView):
    """
    List all movies or creates new one

    """
    queryset = StreamPlatform.objects.all().order_by("id")
    serializer_class = StreamPlatformSerialiser

class StreamPlatformDetailAV(generics.RetrieveUpdateDestroyAPIView):
    """
    Perform all crud update verbs [put, patch, delete]
    """
    queryset = StreamPlatform.objects.all().order_by("id")
    serializer_class = StreamPlatformSerialiser