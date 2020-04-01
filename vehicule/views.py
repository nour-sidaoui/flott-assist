
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Vehicule
from employe.models import Employe, Amende, Conduire

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404

from .models import Vehicule
from employe.views import updated_context
from django.db.models import Q

from .forms import CreerVeh, ModifierVeh
from datetime import datetime


@login_required
def page_vehicules(request):
    return render(request=request,
                  template_name='vehicule/vehicules.html',
                  context=updated_context())


@login_required
def ajouter_veh(request):
    context = updated_context()
    context['creer_veh_form'] = CreerVeh()

    if request.method == 'POST':
        creer_veh_form = CreerVeh(request.POST)

        if creer_veh_form.is_valid():
            creer_veh_form.save()

            messages.success(request, 'Véhicule ajouté avec succès.')
            return redirect('vehicule:page_vehicules')

        else:
            messages.error(request, creer_veh_form.errors)

            # reassign the sent form to context (including errors)
            context['creer_veh_form'] = creer_veh_form

    return render(request=request,
                  template_name='vehicule/ajouter.html',
                  context=context)


@login_required
def fiche_vehicule(request, pk):
    vehicule = get_object_or_404(Vehicule, id=pk)
    veh_filled_form = ModifierVeh(instance=vehicule)

    context = updated_context()
    context['veh_form_modifier'] = veh_filled_form

    if request.POST:
        veh_filled_form = ModifierVeh(request.POST, instance=vehicule)

        if veh_filled_form.is_valid():
            veh_filled_form.save()

            messages.success(request, 'Véhicule modifié avec succès.')
            return redirect('vehicule:page_vehicules')

        else:
            messages.error(request, veh_filled_form.errors)

            # reassign the sent form to context (including errors)
            context['veh_form_modifier'] = veh_filled_form

    return render(request=request,
                  template_name='vehicule/fiche.html',
                  context=context)
