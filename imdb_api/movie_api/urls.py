from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path("movies/", views.MovieListAV.as_view(), name="movies"),
    path("update/<int:pk>/", views.MovieUpdateAV.as_view(), name="update"),
]

urlpatterns = format_suffix_patterns(urlpatterns)