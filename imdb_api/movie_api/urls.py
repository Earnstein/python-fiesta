from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views.watch_list_view import WatchListAV, WatchDetailAV
from .views.streamplatform_View import StreamPlatformListAV ,StreamPlatformDetailAV


urlpatterns = [
    path("list/", WatchListAV.as_view(), name="list"),
    path("list/<int:pk>/", WatchDetailAV.as_view(), name="watchlist-detail"),
    path("stream/", StreamPlatformListAV.as_view(), name="stream"),
    path("stream/<int:pk>/", StreamPlatformDetailAV.as_view(), name="streamplatform-detail"),
]

urlpatterns = format_suffix_patterns(urlpatterns)