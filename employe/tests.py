from django.db.models import signals
from django.test import TestCase

from django.contrib.auth.models import User
from vehicule.models import Vehicule
from .models import Employe, Conduire, Amende

from datetime import datetime


# models.py tests
class UserEmployeeTestCase(TestCase):
    def setUp(self):
        """instantiating User, Employe and Vehicule"""

        # creating user
        User.objects.create_user(username="test1",
                                 first_name="testeur",
                                 last_name="tester")

        # assigning instantiated User to a variable
        created_user = User.objects.get(username="test1")

        # creating employe
        Employe.objects.create(user=created_user,
                               tel="0122334455",
                               adresse="14 rue des allouettes 75019 Paris",
                               email="test@gmail.com",
                               num_permis='342FSU321')

        # assigning instantiated employe to a variable
        created_employe = Employe.objects.get(email="test@gmail.com")

        # creating vehicule
        Vehicule.objects.create(marque="Peugeot",
                                modele="207",
                                annee=2015,
                                immat="FK-654-HF",
                                couleur="Blanc",
                                km=22,
                                prochain_entretien_date="2030-01-01",
                                prochain_entretien_km=1300,
                                validite_assurance="2030-01-01",
                                prochain_controle_technique="2030-01-01",
                                disponible=True)

        # assigning variable to instantiated vehicule
        created_vehicule = Vehicule.objects.get(immat="FK-654-HF")

        # creating conduire
        Conduire.objects.create(id_employe=created_employe,
                                id_vehicule=created_vehicule,
                                km_prise=1300)

        # creating amende
        Amende.objects.create(date=datetime.today(),
                              infraction="vitesse",
                              montant=90,
                              id_employe=created_employe,
                              id_vehicule=created_vehicule)

    def test_employee_added(self):
        """Confirms if Employe exists in db and fields are correct"""
        user = User.objects.get(username="test1")
        self.assertEqual(user.first_name, "testeur")

        employe = Employe.objects.get(email="test@gmail.com")
        self.assertEqual(employe.tel, "0122334455")

    def test_vehicule_added(self):
        """Confirms if Vehicle exists in db and immat field is correct"""
        vehicule = Vehicule.objects.get(immat="FK-654-HF")
        self.assertEqual(vehicule.marque, "Peugeot")

    def test_conduire_added(self):
        """Confirms if Conduire exists in db and km_prise field is correct"""
        employe = Employe.objects.get(email="test@gmail.com")
        vehicule = Vehicule.objects.get(immat="FK-654-HF")
        conduire = Conduire.objects.get(id_employe=employe,
                                        id_vehicule=vehicule)

        self.assertEqual(conduire.km_prise, 1300)

    def test_amende_added(self):
        """Confirms if Amende exists in db and montant field is correct"""
        employe = Employe.objects.get(email="test@gmail.com")
        vehicule = Vehicule.objects.get(immat="FK-654-HF")
        amende = Amende.objects.get(id_employe=employe,
                                    id_vehicule=vehicule)

        self.assertEqual(amende.montant, 90)
