from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from employe.models import Employe, Conduire, Amende
from vehicule.models import Vehicule, Entretien

from django.contrib import messages
from employe.views import updated_context
from .forms import AttribuerVehicule, RestituerVehicule


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
    context['restit_form'] = RestituerVehicule()

    return render(request=request,
                  template_name='dashboard/restituer.html',
                  context=context)


def charger_vehicules(request):
    id_employe = request.GET.get('employe')         # on crée un attribut 'employe' et on l'ajoute à la requête GET
    conduites = Conduire.objects.filter(id_employe=id_employe)
    return render(request, 'droplists/vehicules_dropdown_list_options.html', {'conduites': conduites})

