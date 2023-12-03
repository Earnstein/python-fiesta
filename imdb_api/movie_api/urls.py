from django.urls import path
from . import views


urlpatterns = [
    path("movies/", views.httpGetMovies, name="movies"),
    path("update/<int:pk>/", views.httpUpdateMovie, name="update"),
]
