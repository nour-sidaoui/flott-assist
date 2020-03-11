from django import forms
from .models import Employe


class AjouterCond(forms.ModelForm):

    class Meta:
        model = Employe
        exclude = ('id_vehicule',)

