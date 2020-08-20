from django.test import TestCase

from .models import Vehicule, Entretien
from datetime import datetime


# models.py tests
class VehiculeTestCase(TestCase):
    def setUp(self):
        """instantiating a Vehicule"""

        Vehicule.objects.create(marque="Peugeot",
                                modele="208",
                                annee=2016,
                                immat="DE-342-FS",
                                couleur="Blanc",
                                km=22,
                                prochain_entretien_date="2030-01-01",
                                prochain_entretien_km=1500,
                                validite_assurance="2030-01-01",
                                prochain_controle_technique="2030-01-01",
                                disponible=True)

        # assigning variable to instantiated vehicule
        vehicule = Vehicule.objects.get(immat="DE-342-FS")

        Entretien.objects.create(km=20,
                                 date=datetime.today(),
                                 montant=400.60,
                                 id_vehicule=vehicule)

    def test_vehicule_added(self):
        """Confirms if vehicle exists in db and all fields are correct"""

        vehicule = Vehicule.objects.get(immat="DE-342-FS")

        date_time_str = '01/01/30'
        date_time_obj = datetime.strptime(date_time_str, '%d/%m/%y')

        self.assertEqual(vehicule.marque, "Peugeot")
        self.assertEqual(vehicule.modele, "208")
        self.assertEqual(vehicule.annee, 2016)
        self.assertEqual(vehicule.couleur, "Blanc")
        self.assertEqual(vehicule.prochain_entretien_date, date_time_obj.date())
        self.assertEqual(vehicule.prochain_entretien_km, 1500)
        self.assertEqual(vehicule.validite_assurance, date_time_obj.date())
        self.assertEqual(vehicule.prochain_controle_technique, date_time_obj.date())
        self.assertEqual(vehicule.disponible, True)

    def test_entretien_added(self):
        """Confirms if entretien exists in db and all fields are correct"""
        vehicule = Vehicule.objects.get(immat="DE-342-FS")
        entretien = Entretien.objects.get(id_vehicule=vehicule)

        self.assertEqual(entretien.montant, 400.60)

    def test_entretien_modified(self):
        """Modifies entretien in db and assert that modifications are saved"""
        vehicule = Vehicule.objects.get(immat="DE-342-FS")
        entretien = Entretien.objects.get(id_vehicule=vehicule)

        entretien.montant = 600
        entretien.save()

        self.assertEqual(entretien.montant, 600)

    def test_entretien_deleted(self):
        """deletes entretien in db and assert that the instance no longer exist"""
        vehicule = Vehicule.objects.get(immat="DE-342-FS")
        entretien = Entretien.objects.get(id_vehicule=vehicule)

        entretien.delete()

        with self.assertRaises(Entretien.DoesNotExist):
            Entretien.objects.get(id_vehicule=vehicule)

