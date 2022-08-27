from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from portfolio.filters import ImageFilter
# from rest_framework.decorators import action

from portfolio.models import Comment, Image, Portfolio
from portfolio.permissions import IsAdminOrOwner
from portfolio.serializers import CommentSerializer, ImageSerializer, CreateImageSerializer, PortfolioSerializer


class PortfolioViewSet(ModelViewSet):
    queryset = Portfolio.objects.all()
    lookup_url_kwarg = "portfolio_id"
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    serializer_class = PortfolioSerializer

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)


class ImageViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Image.objects.order_by("-updated_at").all()
    serializer_class = ImageSerializer
    lookup_url_kwarg = "image_id"
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrOwner]


class ImageUploadViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Image.objects.all()
    lookup_url_kwarg = "image_id"
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser]
    filterset_class = ImageFilter

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateImageSerializer
        return ImageSerializer

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = "comment_id"
    permission_classes = [IsAuthenticatedOrReadOnly, IsAdminOrOwner]

    def get_queryset(self):
        return super().get_queryset().filter(image_id=self.kwargs["image_id"])

    def perform_create(self, serializer):
        # TODO: probably can be better. We can remove checking if image exists or not and catch IntegrityError instead.
        image_id = self.kwargs["image_id"]
        if Image.objects.filter(id=image_id).exists():
            return serializer.save(image_id=image_id, user=self.request.user)
        raise APIException({"message": "Image not found"})
