from django import forms
from employe.models import Conduire
from vehicule.models import Vehicule


class AttribuerVehicule(forms.ModelForm):
    class Meta:
        model = Conduire
        fields = '__all__'


class RestituerVehicule(forms.ModelForm):
    class Meta:
        model = Conduire
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_vehicule'].queryset = Vehicule.objects.none()




