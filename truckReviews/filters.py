import django_filters as df
from django import forms
from .models import FoodTruck

class FoodTruckFilter(df.FilterSet):
    def __init__(self, *args, **kwargs):
        super(FoodTruckFilter, self).__init__(*args, **kwargs)
        self.filters['name__icontains'].label = 'Food Truck Name'
        self.filters['category__icontains'].label = 'Category'

    #category_queryset = FoodTruck.objects.exclude(category='').values_list('category', flat=True).distinct().order_by('category')
    #category_drop_down = df.ModelChoiceFilter(queryset=category_queryset)

    class Meta:
        model = FoodTruck
        fields = {
            'name': ['icontains'],
            'category': ['icontains'],
        }
        
        #widget = {
        #    'name': forms.TextInput(attrs={'class': 'form-control'}),
        #    'category': forms.Select(attrs={'class': 'form-control'})
        #}