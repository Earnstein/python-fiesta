from .serlializers import MovieSerialiser
from rest_framework.response import Response
from .models import Movie
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404


class MovieListAV(APIView):
    """
    List all movies or creates new one

    """

    def get(self, request):
        movies = Movie.objects.all().order_by("id")
        movie_serializer = MovieSerialiser(movies, many=True)
        return Response(movie_serializer.data)
       
    def post(self, request):
        movie_serialiser = MovieSerialiser(data=request.data)
        if movie_serialiser.is_valid():
            movie_serialiser.save()
            res = {
                "message": "created",
                "movie": movie_serialiser.data
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(movie_serialiser.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieUpdateAV(APIView):
    """
    Perform all crud update verbs [put, patch, delete]
    """

    def get_object(self, pk):
        try:
            return Movie.objects.get(pk=pk)
        except Movie.DoesNotExist:
            raise Http404

    def get(self, request, pk,  format=None):
            movie = self.get_object(pk)
            movie_serializer = MovieSerialiser(movie)
            return Response(movie_serializer.data)
    

    def patch(self, request, pk, format=None):
        movie = self.get_object(pk)
        movie_serializer = MovieSerialiser(movie, data=request.data)
        if movie_serializer.is_valid():
            movie_serializer.save()
            return Response(movie_serializer.data, status=status.HTTP_200_OK)
        return Response(movie_serializer.errors)

    def delete(self, request, pk, format=None):
        movie = self.get_object(pk)
        movie_serializer  =  MovieSerialiser(movie)
        res = {
            "message":f"{movie.name} is deleted",
            "movie": movie_serializer.data
        }
        movie.delete()
        return Response(res, status=status.HTTP_200_OK)
