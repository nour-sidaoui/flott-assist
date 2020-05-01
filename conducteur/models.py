from django.db import models


class MessageProbleme(models.Model):
    id_employe = models.ForeignKey('employe.Employe', on_delete=models.PROTECT, null=True)
    id_vehicule = models.ForeignKey('vehicule.Vehicule', on_delete=models.PROTECT)
    sent_at = models.DateTimeField(auto_now_add=True)
    sujet = models.CharField(max_length=20, blank=False, null=False)
    text = models.TextField(blank=True, null=True)
    seen = models.BooleanField(default=False)
    solved = models.BooleanField(default=False)
