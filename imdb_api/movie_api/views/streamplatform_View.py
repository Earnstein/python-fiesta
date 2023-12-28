from ..serlializers import StreamPlatformSerialiser
from rest_framework.response import Response
from ..models import StreamPlatform
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404


class StreamPlatformListAV(APIView):
    """
    List all movies or creates new one

    """

    def get(self, request):
        platform = StreamPlatform.objects.all().order_by("id")
        serializer = StreamPlatformSerialiser(platform, many=True,context={'request': request})
        return Response(serializer.data)
       
    def post(self, request):
        serialiser = StreamPlatformSerialiser(data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            res = {
                "message": "created",
                "platform": serialiser.data
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)


class StreamPlatformDetailAV(APIView):
    """
    Perform all crud update verbs [put, patch, delete]
    """

    def get_object(self, pk):
        try:
            return StreamPlatform.objects.get(pk=pk)
        except StreamPlatform.DoesNotExist:
            raise Http404

    def get(self, request, pk,  format=None):
            platform = self.get_object(pk)
            serializer = StreamPlatformSerialiser(platform, context={'request': request})
            return Response(serializer.data)
    

    def patch(self, request, pk, format=None):
        platform = self.get_object(pk)
        serializer = StreamPlatformSerialiser(platform, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        platform = self.get_object(pk)
        serializer  =  StreamPlatformSerialiser(platform)
        res = {
            "message":f"{platform.name} is deleted",
            "movie": serializer.data
        }
        platform.delete()
        return Response(res, status=status.HTTP_200_OK)
