from ..serlializers import WatchListSerialiser
from rest_framework.response import Response
from ..models import Watchlist
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404

class WatchListAV(APIView):
    """
    List all movies or creates new one

    """

    def get(self, request):
        movies = Watchlist.objects.all().order_by("id")
        serializer = WatchListSerialiser(movies, many=True)
        return Response(serializer.data)
       
    def post(self, request):
        serialiser = WatchListSerialiser(data=request.data)
        if serialiser.is_valid():
            serialiser.save()
            res = {
                "message": "created",
                "movie": serialiser.data
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(serialiser.errors, status=status.HTTP_400_BAD_REQUEST)


class WatchDetailAV(APIView):
    """
    Perform all crud update verbs [put, patch, delete]
    """

    def get_object(self, pk):
        try:
            return Watchlist.objects.get(pk=pk)
        except Watchlist.DoesNotExist:
            raise Http404

    def get(self, request, pk,  format=None):
            watchlist = self.get_object(pk)
            serializer = WatchListSerialiser(watchlist)
            return Response(serializer.data)
    

    def patch(self, request, pk, format=None):
        movie = self.get_object(pk)
        serializer = WatchListSerialiser(movie, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors)

    def delete(self, request, pk, format=None):
        movie = self.get_object(pk)
        serializer  =  WatchListSerialiser(movie)
        res = {
            "message":f"{movie.name} is deleted",
            "movie": serializer.data
        }
        movie.delete()
        return Response(res, status=status.HTTP_200_OK)
