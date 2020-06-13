from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from foodtruckreviews import settings

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ContactForm(forms.Form):
    name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True, max_length=50)
    message = forms.CharField(
                                widget=forms.Textarea(
                                    attrs = {
                                        'rows': 4, 
                                        'placeholder': 'Max character length is 500.'
                                    }
                                ), 
                                required=True, 
                                max_length=500
                            )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
        super(ContactForm, self).__init__(*args, **kwargs)

    def send_email(self):
        message = f"Name: {self.cleaned_data.get('name')}"
        message += f"\nEmail: {self.cleaned_data.get('email')}"
        message += f"\n\nMessage:"
        message += f"\n{self.cleaned_data.get('message')}"
        send_mail(
            subject = f"'{self.cleaned_data.get('subject').strip()}' from Contact Form",
            message = message,
            from_email = settings.EMAIL_HOST_USER,
            recipient_list = [settings.EMAIL_HOST_USER] ,
            fail_silently=False
        )