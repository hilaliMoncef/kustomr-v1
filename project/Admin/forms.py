from django.forms import ModelForm
from django.forms import ValidationError
from .models import Training, Message
from Users.models import User
from Vendor.models import Vendor


class TrainingForm(ModelForm):
    class Meta:
        model = Training
        exclude = ['poster']


class VendorSignupForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password', 'first_name', 'last_name')


class MessageForm(ModelForm):
    class Meta:
        model = Message
        exclude = ['vendor']