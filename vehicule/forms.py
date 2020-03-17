from django import forms
from .models import Vehicule


class CreerVeh(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = '__all__'


class ModifierVeh(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = '__all__'