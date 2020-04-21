from django import forms
from django.contrib.auth.forms import UserCreationForm
from Users.models import User


class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=150)
    birthday = forms.DateField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'birthday')