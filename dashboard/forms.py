from django import forms
from employe.models import Employe, Conduire, Amende
from vehicule.models import Vehicule, Entretien

from django.db.models import Q
from datetime import datetime


class AttribuerVehicule(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # filtering available drivers
        conducteurs_en_poste = Employe.objects.filter(Q(date_de_fin__gt=datetime.now()) |
                                                      Q(date_de_fin=None)).values('id')

        busy_drivers = Conduire.objects.filter(date_et_temps_de_prise__isnull=False,
                                               date_et_temps_de_restitution__isnull=True).values('id_employe')

        self.fields['id_employe'].queryset = Employe.objects.filter(id__in=conducteurs_en_poste)\
            .exclude(id__in=busy_drivers)

        # filtering available vehicules
        liste_vehicules_disponibles = Vehicule.objects.filter(disponible=True).values('id')

        busy_vehicules = Conduire.objects.filter(date_et_temps_de_prise__isnull=False,
                                                 date_et_temps_de_restitution__isnull=True).values('id_vehicule')

        self.fields['id_vehicule'].queryset = Vehicule.objects.filter(id__in=liste_vehicules_disponibles)\
            .exclude(id__in=busy_vehicules)

    class Meta:
        model = Conduire
        exclude = ['km_restit',
                   'date_et_temps_de_restitution']


class RestituerVehiculeRecherche(forms.ModelForm):
    class Meta:
        model = Conduire
        fields = ['id_employe',
                  'id_vehicule']

    # overriding initial dropdown state (before AJAX)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_vehicule'].queryset = Vehicule.objects.none()


class RestituerVehicule(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_et_temps_de_restitution'].required = True
        self.fields['km_restit'].required = True
        self.fields['km_restit'].label = 'Km de restitution'

    class Meta:
        model = Conduire
        fields = '__all__'


class AjouterAmende(forms.ModelForm):
    class Meta:
        model = Amende
        fields = '__all__'


class SaisirEntretien(forms.ModelForm):
    class Meta:
        model = Entretien
        fields = '__all__'


