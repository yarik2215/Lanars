from rest_framework.serializers import ModelSerializer, ImageField
from portfolio.models import Comment, Image, Portfolio


class CommentSerializer(ModelSerializer):

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["user", "image", "created_at", "updated_at"]


class ImageSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class CreateImageSerializer(ImageSerializer):
    image = ImageField()


class PortfolioSerializer(ModelSerializer):
    class Meta:
        model = Portfolio
        fields = ["id", "name", "description"]
