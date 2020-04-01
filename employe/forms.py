from django import forms
from .models import Employe

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreerUser(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',
                  'first_name',
                  'last_name',
                  'password1',
                  'password2',
                  ]

    def __init__(self, *args, **kwargs):
        super(CreerUser, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


class ModifierUser(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name',
                  'last_name',
                  'username',
                  ]


class CreerCond(forms.ModelForm):
    class Meta:
        model = Employe
        exclude = ('user',
                   'id_vehicule',
                   'admin',
                   )


class ModifierCond(forms.ModelForm):
    class Meta:
        model = Employe
        exclude = ('user',
                   'id_vehicule',
                   'admin',
                   )
