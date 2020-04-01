from django.db import models


class Vehicule(models.Model):
    marque = models.CharField(max_length=255)
    modele = models.CharField(max_length=255)
    annee = models.IntegerField()
    immat = models.CharField(max_length=9)
    couleur = models.CharField(max_length=255)
    km = models.IntegerField()
    prochain_controle_technique = models.DateField()
    validite_assurance = models.DateField()
    disponible = models.BooleanField()

    def __str__(self):
        full_name = [str(self.marque).capitalize(),
                     str(self.modele).capitalize(),
                     str(self.couleur).capitalize(),
                     str(self.immat).upper()]

        return " ".join(full_name)


class Entretien(models.Model):
    km = models.IntegerField()
    date = models.DateField()
    montant = models.FloatField()
    id_vehicule = models.ForeignKey(Vehicule, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.date) + ' | ' + str(self.montant) + '€'


