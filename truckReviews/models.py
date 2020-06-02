from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class FoodTrucks(models.Model):
    truckID = models.IntegerField(primary_key=True, unique=True, null=False)
    name = models.CharField(max_length=25)
    category = models.CharField(max_length=20)
    bio = models.TextField()
    avatarSRC = models.TextField(default=None)
    avatarALT = models.CharField(max_length=20, default=None)
    avatarTitle = models.CharField(max_length=20, default=None)
    coverPhotoSRC = models.TextField(default=None)
    coverPhotoALT = models.CharField(max_length=20, default=None)
    coverPhotoTitle = models.CharField(max_length=20, default=None)
    website = models.TextField(default=None)
    facebook = models.CharField(max_length=100, default=None)
    instagram = models.CharField(max_length=30, default=None)
    twitter = models.CharField(max_length=15, default=None)


class Review(models.Model):
    reviewID = models.AutoField(primary_key=True, unique=True, serialize=False, null=False)
    truckID = models.ForeignKey(FoodTrucks, on_delete=models.CASCADE)
    userID = models.ForeignKey(User, on_delete=models.CASCADE)
    datePosted = models.DateTimeField(default=timezone.now)
    speedOfService = models.IntegerField()
    qualityAndTaste = models.IntegerField()
    valueForMoney = models.IntegerField()
    comment = models.TextField(max_length=128)