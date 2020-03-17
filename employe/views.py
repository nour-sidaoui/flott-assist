from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404

from .models import Employe
from vehicule.models import Vehicule
from django.db.models import Q

from .forms import CreerUser, CreerCond, ModifierUser, ModifierCond
from datetime import datetime


def updated_context():
    """Remets à jour le dictionnaire contexte et le 'return' """

    liste_vehicules = Vehicule.objects.all()
    liste_vehicules_disponibles = Vehicule.objects.filter(disponible=True)
    liste_conducteurs = Employe.objects.all()
    liste_conducteurs_presents = Employe.objects.filter(Q(date_de_fin__gt=datetime.now()) | Q(date_de_fin=None))

    context = {'liste_vehicules': liste_vehicules,
               'liste_vehicules_disponibles': liste_vehicules_disponibles,
               'liste_conducteurs': liste_conducteurs,
               'liste_conducteurs_presents': liste_conducteurs_presents,
               }
    return context


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login/")


@login_required
def index(request):
    return render(request=request,
                  template_name='employe/index.html',
                  context=updated_context())


@login_required
def page_conducteurs(request):
    return render(request=request,
                  template_name='employe/conducteurs.html',
                  context=updated_context())


@login_required
def ajouter(request):
    if request.method == 'POST':
        creer_user_form = CreerUser(request.POST)
        creer_cond_form = CreerCond(request.POST)

        if creer_user_form.is_valid() and creer_cond_form.is_valid():
            created_user_form = creer_user_form.save()
            created_cond_form = creer_cond_form.save(commit=False)
            created_cond_form.user = created_user_form
            created_cond_form.save()

            messages.success(request, 'Conducteur ajouté avec succès.')
            return redirect('employe:page_conducteurs')

        else:
            messages.error(request, creer_user_form.errors)
            messages.error(request, creer_cond_form.errors)
            return redirect('employe:ajouter_cond')
    else:
        context = updated_context()
        context['creer_user_form'] = CreerUser()
        context['creer_cond_form'] = CreerCond()

    return render(request=request,
                  template_name='employe/ajouter.html',
                  context=context)


@login_required
def voir_profil(request, pk):
    conducteur = get_object_or_404(Employe, id=pk)

    if request.POST:
        user_filled_form = ModifierUser(request.POST, instance=conducteur.user)
        cond_filled_form = ModifierCond(request.POST, instance=conducteur)

        if user_filled_form.is_valid() and cond_filled_form.is_valid():
            user = user_filled_form.save(commit=False)
            cond = cond_filled_form.save()
            cond.user = user
            user.save()
            cond.save()

            messages.success(request, 'Conducteur modifié avec succès.')
            return redirect('employe:voir_profil', pk=pk)

        else:
            messages.error(request, user_filled_form.errors)
            messages.error(request, cond_filled_form.errors)
    else:
        user_filled_form = ModifierUser(instance=conducteur.user)
        cond_filled_form = ModifierCond(instance=conducteur)

    context = updated_context()
    context['user_form_modifier'] = user_filled_form
    context['cond_form_modifier'] = cond_filled_form

    return render(request=request,
                  template_name='employe/profil.html',
                  context=context)
