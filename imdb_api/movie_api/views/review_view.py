from rest_framework import mixins
from rest_framework import generics
from ..serlializers import ReviewSerialiser
from ..models import Review
from rest_framework import status

class ReviewListAPIView(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
    """
    List all reviews or creates new one

    """
    queryset = Review.objects.all().order_by("id")
    serializer_class = ReviewSerialiser

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return self.custom_response(response, "Review created successfully")

    def custom_response(self, response, message):
        if response.status_code == status.HTTP_201_CREATED:
            data = response.data
            response.data = {'message': message, **data}
        return response


class ReviewUpdateAPIView(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    """
    performs crud on a single review

    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerialiser

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)