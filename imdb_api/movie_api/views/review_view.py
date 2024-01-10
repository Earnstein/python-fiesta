from rest_framework import generics
from ..serlializers import ReviewSerialiser
from ..models import Review, Watchlist



class ReviewCreate(generics.CreateAPIView):
    serializer_class = ReviewSerialiser

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie = Watchlist.objects.get(pk=pk)
        serializer.save(watchlist=movie)

class ReviewList(generics.ListAPIView):
    """
    List all reviews or creates new one

    """
    # queryset = Review.objects.all().order_by("id")
    serializer_class = ReviewSerialiser

    def get_queryset(self):
        pk = self.kwargs['pk']
        review = Review.objects.filter(watchlist=pk)
        return review


class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    performs crud on a single review

    """
    queryset = Review.objects.all().order_by("id")
    serializer_class = ReviewSerialiser