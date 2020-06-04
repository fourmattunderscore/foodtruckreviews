from django import forms
from .models import Review
from django.utils.translation import ugettext_lazy as _

class ReviewForm(forms.ModelForm):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for field in self.fields.values():
            if not field.widget.is_hidden:
                field.widget.attrs.setdefault("class", "form-control")

    class Meta:
        model = Review
        ordering = ['-posted_at']
        fields = ('speed_of_service', 'quality_and_taste', 'value_for_money', 'comment')
        exclude = ("uuid", "user", "food_truck", "posted_at")
        labels = {
            'speed_of_service': _('Speed Of Service'),
            'quality_and_taste': _('Quality And Taste'),
            'value_for_money': _('Value For Money')
        }
        error_messages = {
            'comment': {
                'max_length': _('This comment is too long, maximum length is 128 characters.')
            }
        }
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2})
        }

#label='Speed Of Service', widget=forms.Select(choices=intChoice)