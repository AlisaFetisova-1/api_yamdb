
from rest_framework import  viewsets
from django.contrib.auth import get_user_model

from rest_framework.generics import get_object_or_404

from reviews.models import Comment, Review, Title

from .paginators import FourPerPagePagination
from .permissions import (AdminOrSuperuser, IsAdminOrReadOnly,
                          IsUserAnonModerAdmin)
from .serializers import (CommentSerializer, ReviewSerializer)

User = get_user_model()

class ReViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserAnonModerAdmin]
    serializer_class = ReviewSerializer
    pagination_class = FourPerPagePagination

    def _get_title(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def get_queryset(self):
        return Review.objects.filter(
            title_id=self.kwargs.get('title_id')
        ).select_related('author')

    def perform_create(self, serializer):
        title = self._get_title()
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsUserAnonModerAdmin]
    serializer_class = CommentSerializer
    pagination_class = FourPerPagePagination

    def _get_review(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'])

    def get_queryset(self):
        return Comment.objects.filter(
            review__title_id=self.kwargs.get('title_id'),
            review_id=self.kwargs.get('review_id')
        ).select_related('author')

    def perform_create(self, serializer):
        review = self._get_review()
        author = self.request.user
        serializer.save(author=author, review=review)
