from PIL import Image
from math import floor

from django import forms
from .models import Employe, Photo

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

    def __init__(self, *args, **kwargs):
        super(ModifierUser, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = None


class CondForm(forms.ModelForm):
    class Meta:
        model = Employe
        exclude = ('user',
                   'id_vehicule',
                   'admin',
                   'id_photo',
                   'is_admin',
                   )


class ModifierCond(forms.ModelForm):
    class Meta:
        model = Employe
        exclude = ('user',
                   'id_vehicule',
                   'admin',
                   'id_photo',
                   )


class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    w = forms.FloatField(widget=forms.HiddenInput())
    h = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        fields = ('picture', 'x', 'y', 'w', 'h', )

    def __init__(self, *args, **kwargs):
        super(PhotoForm, self).__init__(*args, **kwargs)
        self.fields['picture'].label = False

    def crop_and_save(self):
        photo = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('w')
        h = self.cleaned_data.get('h')

        image = Image.open(photo.picture)

        # checking if inputs have been added (using 'w' in case 'x' == 0)
        if w:
            cropped_image = image.crop((x,
                                        y,
                                        floor(x + w),
                                        floor(y + h)
                                        ))

        # cropping to a default square otherwise
        else:
            # cropping on the smallest size (width based)
            if image.width < image.height:
                cropped_image = image.crop((0, 0, image.width, image.width))

            # cropping on the smallest size (height based)
            elif image.width > image.height:
                cropped_image = image.crop((0, 0, image.height, image.height))

            # if image is already 1/1 aspect ratio
            elif image.width == image.height:
                cropped_image = image

            else:
                raise IOError

        resized_image = cropped_image.resize((200, 200), Image.ANTIALIAS)
        resized_image.save(photo.picture.path)

        return photo

