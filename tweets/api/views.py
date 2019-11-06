from rest_framework import generics
from .serializers import TweetModelSerializer
from tweets.models import Tweet
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from .pagination import StandardResultsPagination

class TweetListAPIView(generics.ListAPIView):
    serializer_class = TweetModelSerializer
    # PAGINATION
    pagination_class = StandardResultsPagination

    def get_queryset(self, *args, **kwargs):
        qs = Tweet.objects.all().order_by("-timestamp")
        #print(self.request.GET)
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs


class TweetCreateAPIView(generics.CreateAPIView):
    serializer_class = TweetModelSerializer
    # don't allow anonymous user
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        """Create a new tweet"""
        serializer.save(user=self.request.user)
