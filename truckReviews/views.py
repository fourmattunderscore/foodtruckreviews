from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from .models import FoodTruck, Review
from .forms import ReviewForm

import typing as t
if t.TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse
    from django.contrib.auth.models import AbstractUser

    class AuthenticatedRequest(HttpRequest):
        user: AbstractUser = ...

class TruckListView(generic.ListView):
    model = FoodTruck
    template_name = 'truckReviews/landing.html' # <app>/<model>_<viewtype>.html <-- Base Django Convention
    context_object_name = 'trucks' # object_list <-- Base Django Convention
    ordering = 'name'
    paginate_by = 9

class UserReviewListView(LoginRequiredMixin, UserPassesTestMixin, generic.ListView):
    model = Review
    template_name = 'users/userReviews.html'
    paginate_by = 10

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Review.objects.filter(user=user.id).order_by('food_truck')
    
    def test_func(self):
        if self.request.user.username == self.kwargs.get('username'):
            return True
        return False

class FoodTruckDetailReviewListCreateView(
    generic.list.MultipleObjectMixin, generic.edit.CreateView,
):
    template_name = "truckReviews/createTruckReview.html"
    model = Review
    list_model = Review
    context_list_name = "reviews"
    context_object_name = "foodtruck"
    detail_model = FoodTruck
    form_class = ReviewForm

    def get(self, request: "AuthenticatedRequest", *args, **kwargs) -> "HttpResponse":
        """
        Combine the work of BaseListView and BaseDetailView

        Combines the get implementation of BaseListView and BaseDetailView, but
        without the response rendering. Then hands over control to CreateView's
        method to do the final rendering.

        Some functionality is stripped, because we don't need it.

        :param request: The incoming request
        :return: A response, which can be a redirect
        """
        # BaseListView
        self.object_list = self.get_queryset()
        # BaseDetailView
        self.object = self.get_object()
        context = self.get_context_data(
            object=self.object, object_list=self.object_list
        )
        # CreateView sets self.object to None, but we override form_kwargs, so
        # we can leave it at a value.

        return self.render_to_response(context=context)

    def get_template_names(self):
        # Bypass logic in superclasses that we don't need
        return [self.template_name]

    def get_object(self, queryset=None):
        # We provide the queryset to superclasses with the other model
        return super().get_object(queryset=self.detail_model.objects.all())

    def get_queryset(self):
        # This only gets called by MultipleObjectMixin
        global pk
        pk = self.kwargs.get(self.pk_url_kwarg)
        if pk is None:
            raise AttributeError(
                "Unable to filter on food truck: {} is missing in url.".format(
                    self.pk_url_kwarg
                )
            )
        queryset = self.list_model.objects.filter(food_truck_id=pk)
        # print(str(queryset.query))
        return queryset

    def get_context_data(self, **kwargs):
        if "object" in kwargs:
            kwargs[self.context_object_name] = kwargs["object"]
        if "object_list" in kwargs:
            kwargs[self.context_list_name] = kwargs["object_list"]

        return super().get_context_data(**kwargs)

    def get_form_kwargs(self):
        # Bypass ModelFormMixin, which passes in self.object as instance if it
        # is set.
        return super(generic.edit.ModelFormMixin, self).get_form_kwargs()
    
    def form_valid(self, form):
        global pk
        form.instance.user = self.request.user
        form.instance.food_truck_id = pk
        return super().form_valid(form)

class About(generic.TemplateView):
    template_name = 'truckReviews/about.html'

import json
import requests
from django.http import HttpResponse

def update(request):
    unfiltered_json = requests.get("https://www.bnefoodtrucks.com.au/api/1/trucks")
    foodTruck_dictionary = json.loads(unfiltered_json.text)
    for i in foodTruck_dictionary:
        i = FoodTruck(
                    truck=i['truck_id'], name=i['name'], category=i['category'], bio=i['bio'], 
                    avatar_url=i['avatar']['src'], avatar_alt_text=i['avatar']['alt'], avatar_title=i['avatar']['title'],
                    cover_photo_url=i['cover_photo']['src'], cover_photo_alt_text=i['cover_photo']['alt'], cover_photo_title=i['cover_photo']['title'],
                    website=i['website'], facebook=i['facebook_url'], instagram=i['instagram_handle'], twitter=i['twitter_handle']
                    )
        i.save()

    return HttpResponse("API Imported")