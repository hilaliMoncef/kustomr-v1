from django.forms import ModelForm
from django.forms import ValidationError
from .models import Training


class TrainingForm(ModelForm):
    class Meta:
        model = Training
        exclude = ['poster']