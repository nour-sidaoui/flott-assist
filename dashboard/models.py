from django.db import models

from vehicule.models import Vehicule


class Notification(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    id_vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, null=True)
    is_ct = models.BooleanField(default=False)
    is_entretien = models.BooleanField(default=False)
    is_assurance = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)

    def __str__(self):
        if self.is_ct:
            return 'Contrôle technique de la ' + str(self.id_vehicule)

        if self.is_entretien:
            return 'Entretien pour la ' + str(self.id_vehicule)

        if self.is_assurance:
            return 'Assurance à renouveler pour la ' + str(self.id_vehicule)

        else:
            return self
