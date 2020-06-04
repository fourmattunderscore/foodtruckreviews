from django.urls import path
from . import views
from .views import About, TruckListView, FoodTruckDetailReviewListCreateView, update #TruckCreateReviewView, TruckReviewListView

urlpatterns = [
    path('', TruckListView.as_view(), name='reviews-home'),
    path('truck/<int:pk>/', FoodTruckDetailReviewListCreateView.as_view(), name='truck-review'),
    path('about/', About.as_view(), name='reviews-about'),
    path('updateAPI/', update, name='update-api')
]