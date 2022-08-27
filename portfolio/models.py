from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from utils.models import TimestampModelMixin


class Portfolio(TimestampModelMixin, models.Model):
    name = models.CharField(_("name"), max_length=255)
    description = models.TextField(_("description"), max_length=2000)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="portfolios")

    # Reverse related fields
    #images
    

class Image(TimestampModelMixin, models.Model):
    name = models.CharField(_("name"),max_length=255)
    description = models.TextField(_("description"),max_length=2000)
    image = models.ImageField(_("image"))
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="images")

    # Reverse related fields
    #comments


class Comment(TimestampModelMixin, models.Model):
    text = models.TextField(_("text"), max_length=2000)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="comments")
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="comments")
