import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class FoodTruck(models.Model):
    truck = models.IntegerField(primary_key=True, unique=True, null=False)
    name = models.CharField(max_length=25)
    category = models.CharField(max_length=20)
    bio = models.TextField()
    avatar_url = models.URLField(blank=True)
    avatar_alt_text = models.CharField(max_length=20, blank=True)
    avatar_title = models.CharField(max_length=20, blank=True)
    cover_photo_url = models.URLField(blank=True)
    cover_photo_alt_text = models.CharField(max_length=20, default="No photo provided")
    cover_photo_title = models.CharField(max_length=20, default="No photo provided")
    website = models.URLField(blank=True, null=True)
    facebook = models.URLField(max_length=100, blank=True, null=True)
    instagram = models.CharField(max_length=30, blank=True, null=True)
    twitter = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

#class Review(models.Model):
#    review = models.AutoField(primary_key=True, unique=True, serialize=False, null=False)
#    truck = models.ForeignKey(FoodTrucks, on_delete=models.CASCADE)
#    user = models.ForeignKey(User, on_delete=models.CASCADE)
#    datePosted = models.DateTimeField(default=timezone.now)
#    speedOfService = models.IntegerField()
#    qualityAndTaste = models.IntegerField()
#    valueForMoney = models.IntegerField()
#    comment = models.TextField(max_length=128)

    #def get_absolute_url(self):
    #    return reverse('truck-detail', kwargs={'pk': self.pk})

#models.ChoiceField(intChoice)

intChoice = [(1, 'Positive'),(0, 'Neutral'),(-1, 'Negative')]

class Review(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    food_truck = models.ForeignKey(
        FoodTruck, on_delete=models.CASCADE, related_name="reviews", default=None
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    posted_at = models.DateTimeField(default=timezone.now)
    speed_of_service = models.IntegerField(default=intChoice, choices=intChoice)
    quality_and_taste = models.IntegerField(default=intChoice, choices=intChoice)
    value_for_money = models.IntegerField(default=intChoice, choices=intChoice)
    comment = models.TextField(max_length=128, blank=True, null=True)

    def __str__(self):
        return "Review about {} by {}".format(
            self.food_truck.name, self.user.get_full_name()
        )

    def get_absolute_url(self):
        return reverse('truck-review', kwargs={'pk': self.food_truck.truck})