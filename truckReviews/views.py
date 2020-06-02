from django.shortcuts import render
from .models import FoodTrucks

def home(request):
    context = {
        'trucks': FoodTrucks.objects.all().order_by('name')
    }
    return render(request, 'truckReviews/landing.html', context)

def about(request):
    return render(request, 'truckReviews/about.html')