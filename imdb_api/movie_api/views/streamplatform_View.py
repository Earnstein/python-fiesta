from ..serlializers import StreamPlatformSerialiser
from ..models import StreamPlatform
from rest_framework import generics

class StreamPlatformList(generics.ListCreateAPIView):
    """
    List all movies or creates new one

    """
    queryset = StreamPlatform.objects.all().order_by("id")
    serializer_class = StreamPlatformSerialiser

class StreamPlatformDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Perform all crud update verbs [put, patch, delete]
    """
    queryset = StreamPlatform.objects.all().order_by("id")
    serializer_class = StreamPlatformSerialiser