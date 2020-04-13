from django import forms
from .models import MessageProbleme
from employe.models import Conduire
from datetime import datetime

from django.db import models
from django.forms import Textarea


class FormConduirePrise(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormConduirePrise, self).__init__(*args, **kwargs)
        self.fields['km_prise'].label = 'Km prise'

    class Meta:
        model = Conduire
        fields = ['km_prise',
                  ]


class FormConduireRestit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormConduireRestit, self).__init__(*args, **kwargs)
        self.fields['km_restit'].label = 'Km de restitution'
        initial = {'date_et_temps_de_restitution': datetime.now()}
        self.initial = initial

    class Meta:
        model = Conduire
        fields = ['km_restit',
                  'date_et_temps_de_restitution',
                  ]


class FormMessage(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormMessage, self).__init__(*args, **kwargs)
        self.fields['text'].label = 'Details (facultatif)'

    class Meta:
        model = MessageProbleme
        fields = ('sujet',
                  'text',)
