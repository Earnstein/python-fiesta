from .serlializers import MovieSerialiser
from rest_framework.response import Response
from .models import Movie
from rest_framework.decorators import api_view
from rest_framework import status
# Create your views here.

@api_view(["GET", "POST"])
def httpGetMovies(request):

    if request.method == "GET":
        movies = Movie.objects.all().order_by("id")
        movie_serializer = MovieSerialiser(movies, many=True)
        return Response(movie_serializer.data)

    if request.method == "POST":
        movie_serialiser = MovieSerialiser(data=request.data)
        if movie_serialiser.is_valid():
            movie_serialiser.save()
            res = {
                "message": "created",
                "movie": movie_serialiser.data
            }
            return Response(res, status=status.HTTP_201_CREATED)
        return Response(movie_serialiser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def httpUpdateMovie(request, pk):
    if request.method == "GET":
        try:
            movie = Movie.objects.get(pk=pk)
            movie_serializer = MovieSerialiser(movie)
            return Response(movie_serializer.data)
        except Movie.DoesNotExist:
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PATCH":
        try:
            movie = Movie.objects.get(pk=pk)
            movie_serializer = MovieSerialiser(movie, data=request.data)
            if movie_serializer.is_valid():
                movie_serializer.save()
                return Response(movie_serializer.data, status=status.HTTP_200_OK)
            return Response(movie_serializer.errors)
        except Movie.DoesNotExist:
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "PUT":
        try:
            movie = Movie.objects.get(pk=pk)
            movie_serializer = MovieSerialiser(movie, data=request.data)
            if movie_serializer.is_valid():
                movie_serializer.save()
                return Response(movie_serializer.data, status=status.HTTP_200_OK)
            return Response(movie_serializer.errors)
        except Movie.DoesNotExist:
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "DELETE":
        try:
            movie = Movie.objects.get(pk=pk)
            movie_serializer  =  MovieSerialiser(movie)
            res = {
                "message":f"{movie.name} is deleted",
                "movie": movie_serializer.data
            }
            movie.delete()
            return Response(res, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({"message": "not found"}, status=status.HTTP_404_NOT_FOUND)