from django.db import models

from django.contrib.auth.models import User
from datetime import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):

    # triggering if instance is created and is superuser
    if created and instance.is_superuser:
        Token.objects.create(user=instance)


class Photo(models.Model):
    picture = models.ImageField(upload_to='profils', default='media/default.png')

    class Meta:
        verbose_name = 'photo'
        verbose_name_plural = 'photos'


class Employe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tel = models.CharField(max_length=10)
    adresse = models.CharField(max_length=255)
    email = models.EmailField(max_length=50)
    num_permis = models.CharField(max_length=9, null=True)
    date_de_debut = models.DateField(null=True)
    date_de_fin = models.DateField(null=True, blank=True)
    id_vehicule = models.ManyToManyField('vehicule.Vehicule', through='Conduire', blank=True)
    id_photo = models.OneToOneField(Photo, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        full_name = [str(self.user.first_name).capitalize(),
                     str(self.user.last_name).upper()]
        return " ".join(full_name)


class Conduire(models.Model):
    id_employe = models.ForeignKey(Employe, on_delete=models.PROTECT)
    id_vehicule = models.ForeignKey('vehicule.Vehicule', on_delete=models.PROTECT)
    km_prise = models.IntegerField(null=True, blank=True)
    date_et_temps_de_prise = models.DateTimeField(null=False, blank=False, default=datetime.now)  # no () to run in time
    km_restit = models.IntegerField(null=True, blank=True)
    date_et_temps_de_restitution = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Conduire"


class Amende(models.Model):
    date = models.DateField()
    infraction = models.CharField(max_length=255)
    montant = models.IntegerField()
    id_employe = models.ForeignKey(Employe, on_delete=models.PROTECT)
    id_vehicule = models.ForeignKey('vehicule.Vehicule', on_delete=models.PROTECT)

