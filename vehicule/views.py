from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Vehicule
from employe.models import Employe, Amende, Conduire


def updated_context():
    """Remets à jour le dictionnaire contexte et le 'return' """
    liste_admin = Employe.objects.filter(admin=True)
    liste_conducteurs = Employe.objects.filter(admin=False)
    liste_vehicules = Vehicule.objects.all()

    context = {'liste_vehicules': liste_vehicules,
               'liste_admin': liste_admin,
               'liste_conducteurs': liste_conducteurs,
               'num_employe': Employe.num_employe,
               'vehicule.id': id,
               }
    return context


def page_vehicules(request):
    return render(request, 'vehicule/vehicules.html', updated_context())


def ajouter(request):
    return HttpResponse("Page ajouter vehicule.")


def fiche_vehicule(request, veh_id):
    return HttpResponse("<h1>Vous êtes sur la page du vehicule immat: %s.</h1>" % Vehicule.objects.get(id=veh_id))
