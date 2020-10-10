from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class AuctionListing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    startingBid = models.FloatField()
    imageUrl = models.CharField(max_length=256)
    category = models.CharField(max_length=64)

class Bid(models.Model):
    pass


class Comment(models.Model):
    pass