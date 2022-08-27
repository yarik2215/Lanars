from django.urls import path, include
from rest_framework.routers import DefaultRouter

from portfolio.views import ImageViewSet, CommentViewSet, ImageUploadViewSet, PortfolioViewSet

router = DefaultRouter()
router.register(r"images", ImageViewSet)
router.register(r"images", ImageUploadViewSet)
router.register(r"portfolios", PortfolioViewSet)

comment_router = DefaultRouter()
comment_router.register(r"comments", CommentViewSet)

urlpatterns = [
    *router.urls,
    path("images/<int:image_id>/", include(comment_router.urls))
]
