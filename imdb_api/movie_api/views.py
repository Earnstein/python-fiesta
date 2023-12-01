from django.shortcuts import render
from django.http import JsonResponse
from .models import Movie
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def httpGetMovies(request):
    all_movies = Movie.objects.all()
    json_data = {
        'movies': list(all_movies.values())
    }
    return JsonResponse(json_data)

@csrf_exempt
@require_POST
def httpCreateMovie(request):
    print(request.POST)
    movie_name = request.POST['movie_name']
    description = request.POST['description']
    if movie_name != '' and description != '':
        new_movie = Movie.objects.create(
            name=movie_name, 
            description=description
        )
        new_movie.active = True
        new_movie.save()
        return JsonResponse({
            'message': "data succussfully saved"
        })
    
    return JsonResponse({
            'message': "invalid data"
        })