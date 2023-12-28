from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views.watchlist_view import WatchListAV, WatchDetailAV
from .views.streamplatform_View import StreamPlatformListAV ,StreamPlatformDetailAV
from .views.review_view import ReviewListAPIView, ReviewUpdateAPIView


urlpatterns = [
    path("list/", WatchListAV.as_view(), name="list"),
    path("list/<int:pk>/", WatchDetailAV.as_view(), name="watchlist-detail"),
    path("stream/", StreamPlatformListAV.as_view(), name="stream"),
    path("stream/<int:pk>/", StreamPlatformDetailAV.as_view(), name="streamplatform-detail"),
    path("review/", ReviewListAPIView.as_view(), name="review"),
    path("review/<int:pk>/", ReviewUpdateAPIView.as_view(), name="review-detail")
]

urlpatterns = format_suffix_patterns(urlpatterns)