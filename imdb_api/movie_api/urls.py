from django.urls import path
from . import views


urlpatterns = [
    path("movies/", views.httpGetMovies, name="movies"),
    path("create/", views.httpCreateMovie, name="create")  
]
