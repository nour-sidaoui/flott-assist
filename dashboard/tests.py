from django.test import TestCase

from vehicule.models import Vehicule
from .models import Notification
from .views import notification_factory

from datetime import datetime, timedelta


class UserEmployeeTestCase(TestCase):
    def setUp(self):
        """instantiating Vehicules with upcoming 'controle technique', 'assurance' & 'entretien' """

        in_two_weeks = datetime.today() + timedelta(days=14)
        in_one_year = datetime.today() + timedelta(days=365)

        # creating vehicules
        Vehicule.objects.create(marque="Peugeot",
                                modele="208",
                                annee=2015,
                                immat="GT-650-HS",
                                couleur="Blanc",
                                km=24312,
                                prochain_entretien_date=in_two_weeks,
                                prochain_entretien_km=35000,
                                validite_assurance=in_two_weeks,
                                prochain_controle_technique=in_two_weeks,
                                disponible=True)
        
        Vehicule.objects.create(marque="Renault",
                                modele="Kangoo",
                                annee=2015,
                                immat="GF-404-OP",
                                couleur="Noir",
                                km=244890,
                                prochain_entretien_date=in_one_year,
                                prochain_entretien_km=245000,
                                validite_assurance=in_one_year,
                                prochain_controle_technique=in_one_year,
                                disponible=True)

    def test_notification_factory(self):
        notification_factory()

        created_vehicule1 = Vehicule.objects.get(immat="GT-650-HS")
        created_vehicule2 = Vehicule.objects.get(immat="GF-404-OP")

        # testing notification: controle technique
        notif_ct = Notification.objects.get(id_vehicule=created_vehicule1,
                                            is_ct=True)
        self.assertEqual(notif_ct.is_ct, True)

        # testing notification: entretien (date)
        notif_entretien = Notification.objects.get(id_vehicule=created_vehicule1,
                                                   is_entretien=True)
        self.assertEqual(notif_entretien.is_entretien, True)

        # testing notification: entretien (km)
        notif_entretien = Notification.objects.get(id_vehicule=created_vehicule2,
                                                   is_entretien=True)
        self.assertEqual(notif_entretien.is_entretien, True)

        # testing notification: assurance
        notif_assurance = Notification.objects.get(id_vehicule=created_vehicule1,
                                                   is_assurance=True)
        self.assertEqual(notif_assurance.is_assurance, True)
