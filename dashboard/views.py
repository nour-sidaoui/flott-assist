from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse, HttpResponseRedirect

from employe.models import Employe, Conduire, Amende
from vehicule.models import Vehicule, Entretien

from django.contrib import messages
from employe.views import updated_context
from .forms import AttribuerVehicule, RestituerVehiculeRecherche, RestituerVehicule
from django.db.models import Q


@login_required
def index(request):
    return render(request=request,
                  template_name='dashboard/index.html',
                  context=updated_context())


@login_required
def attribuer_veh(request):
    if request.method == 'POST':
        attribuer_form = AttribuerVehicule(request.POST)

        if attribuer_form.is_valid():
            attribuer_form.save()

            messages.success(request, 'Vehicule attribué avec succès.')
            return redirect('dashboard:index')

        else:
            messages.error(request, attribuer_form.errors)
            return redirect('dashboard:attribuer_vehicule')

    context = updated_context()
    context['attribuer_form'] = AttribuerVehicule()

    return render(request=request,
                  template_name='dashboard/attribuer.html',
                  context=context)


@login_required
def restituer_veh(request):
    context = updated_context()

    if request.POST:
        # si le conducteur et vehicules on déjà étés selectionnés
        if 'km_prise' in request.POST:
            conduire = get_object_or_404(Conduire,
                                         id_employe=request.POST.get('id_employe'),
                                         id_vehicule=request.POST.get('id_vehicule'),
                                         km_prise=request.POST.get('km_prise'))
            restit_form = RestituerVehicule(request.POST, instance=conduire)

            if restit_form.is_valid():
                restit_form.save()

                messages.success(request, 'Le véhicule à été réstitué avec succès.')
                return redirect('dashboard:index')

            # si le formulaire n'est pas valide
            else:
                messages.error(request, restit_form.errors)
                return redirect('dashboard:restituer_vehicule')

        # si le conducteur et véhicule n'ont pas encore étés selectionnés (requête GET)
        else:
            conduire = get_object_or_404(Conduire,
                                         id_employe=request.POST.get('recherche_cond'),
                                         id_vehicule=request.POST.get('recherche_veh'),
                                         km_restit=None)
            context['restit_form'] = AttribuerVehicule(instance=conduire)

    context['restit_form_rechercher'] = RestituerVehiculeRecherche()
    context['liste_conducteurs_en_mission'] = Conduire.objects.filter(date_et_temps_de_prise__isnull=False,
                                                                      date_et_temps_de_restitution__isnull=True)
    return render(request=request,
                  template_name='dashboard/restituer.html',
                  context=context)


def charger_vehicules(request):
    id_employe = request.GET.get('employe')
    conduites = Conduire.objects.filter(id_employe=id_employe)

    return render(request=request,
                  template_name='droplists/vehicules_dropdown_list_options.html',
                  context={'conduites': conduites})

