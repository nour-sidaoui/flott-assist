from django.db import models


class Vehicule(models.Model):
    marque = models.CharField(max_length=255)
    modele = models.CharField(max_length=255)
    annee = models.IntegerField()
    immat = models.CharField(max_length=9)
    couleur = models.CharField(max_length=255)
    km = models.IntegerField()
    disponible = models.BooleanField()

    def __str__(self):
        return str(self.immat).upper()


class Entretien(models.Model):
    date = models.DateField()
    montant = models.FloatField()
    id_vehicule = models.ForeignKey(Vehicule, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.date) + ' | ' + str(self.montant) + '€'


