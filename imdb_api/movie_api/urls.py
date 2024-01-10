from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views.watchlist_view import WatchListAV, WatchDetailAV
from .views.streamplatform_View import StreamPlatformList ,StreamPlatformDetail
from .views.review_view import ReviewCreate, ReviewList, ReviewDetail


urlpatterns = [
    path("list/", WatchListAV.as_view(), name="list"),
    path("list/<int:pk>/", WatchDetailAV.as_view(), name="watchlist-detail"),


    path("stream/", StreamPlatformList.as_view(), name="streamplatform-list"),
    path("stream/<int:pk>/", StreamPlatformDetail.as_view(), name="streamplatform-detail"),

    path("stream/<int:pk>/post-review/", ReviewCreate.as_view(), name="create-review"),
    path("stream/<int:pk>/review/", ReviewList.as_view(), name="review-list"),
    path("stream/review/<int:pk>/", ReviewDetail.as_view(), name="review-detail"),
    
    # path("review/", ReviewList.as_view(), name="review"),
    # path("review/<int:pk>/", ReviewDetail.as_view(), name="review-detail")
]

urlpatterns = format_suffix_patterns(urlpatterns)