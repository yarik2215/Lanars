from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Portfolio(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="portfolios")

    # Reverse related fields
    #images
    

class Image(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    image = models.ImageField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name="images")

    # Reverse related fields
    #comments


class Comment(models.Model):
    text = models.TextField(max_length=2000)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="comments")
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name="comments")
