from django.forms import ModelForm
from django.forms import ValidationError
from .models import Training
from Users.models import User


class TrainingForm(ModelForm):
    class Meta:
        model = Training
        exclude = ['poster']


class VendorSignupForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')