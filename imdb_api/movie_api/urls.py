from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views.watch_list_view import WatchListAV, WatchDetailAV
from .views.streamplatform_View import StreamPlatformListAV ,StreamPlatformDetailAV


urlpatterns = [
    path("movies/", WatchListAV.as_view(), name="movies"),
    path("update_movies/<int:pk>/", WatchDetailAV.as_view(), name="update"),
    path("stream/", StreamPlatformListAV.as_view(), name="streams"),
    path("update_stream/<int:pk>/", StreamPlatformDetailAV.as_view(), name="update_streams"),
]

urlpatterns = format_suffix_patterns(urlpatterns)