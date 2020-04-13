from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404

from .forms import AttribuerVehicule, RestituerVehiculeRecherche, RestituerVehicule, AjouterAmende, SaisirEntretien
from django.db.models import Q

from employe.models import Employe, Conduire
from vehicule.models import Vehicule
from conducteur.models import MessageProbleme

import datetime


def updated_context():
    """Remets à jour le dictionnaire contexte et le 'return' """
    liste_messages_non_lus = sorted(MessageProbleme.objects.filter(seen=False), key=lambda m: m.sent_at, reverse=True)
    liste_messages_lus = sorted(MessageProbleme.objects.filter(seen=True), key=lambda m: m.sent_at, reverse=True)

    liste_vehicules = Vehicule.objects.all().order_by('marque')
    liste_vehicules_disponibles = Vehicule.objects.filter(disponible=True)

    liste_conducteurs = sorted(Employe.objects.all(), key=lambda m: m.user.first_name.lower())
    liste_conducteurs_presents = sorted(Employe.objects.filter(Q(date_de_fin__gt=datetime.datetime.now()) | Q(date_de_fin=None)),
                                        key=lambda m: m.user.first_name.lower())

    context = {'liste_messages_non_lus': liste_messages_non_lus,
               'liste_messages_lus': liste_messages_lus,

               'liste_vehicules': liste_vehicules,
               'liste_vehicules_disponibles': liste_vehicules_disponibles,

               'liste_conducteurs': liste_conducteurs,
               'liste_conducteurs_presents': liste_conducteurs_presents,
               }
    return context


def is_admin(user):
    """vérifie que le user est un superuser (admin)"""
    return user.is_superuser


@login_required
def index(request):
    # redirecting non-admins to conducteur's index
    if not request.user.is_superuser:
        return redirect("conducteur:index")

    conduites = Conduire.objects.filter(Q(date_et_temps_de_prise__isnull=False) and
                                        Q(date_et_temps_de_restitution__isnull=True))

    # filtering events in the next 30 days
    upcoming_month = datetime.date.today() + datetime.timedelta(days=30)
    liste_controles_tech = Vehicule.objects.filter(prochain_controle_technique__lte=upcoming_month)

    # gathering all messages
    msgs = sorted(MessageProbleme.objects.all(), key=lambda m: m.sent_at, reverse=True)

    # gathering vehicles' issues
    issues = []
    for conduite in conduites:
        issue = MessageProbleme.objects.filter(id_vehicule=conduite.id_vehicule,
                                               solved=False)
        if len(issue) > 1:
            issues.append(issue.latest('sent_at'))
        else:
            issues.append(issue)

    context = updated_context()
    context['liste_controles_tech'] = liste_controles_tech
    context['conduites'] = conduites
    context['msgs'] = msgs
    context['issues'] = issues

    return render(request=request,
                  template_name='dashboard/index.html',
                  context=context)


@login_required
@user_passes_test(is_admin)
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
@user_passes_test(is_admin)
def restituer_veh(request):
    context = updated_context()

    if request.POST:
        # si le conducteur et vehicules on déjà étés selectionnés
        if 'km_prise' in request.POST:
            conduire = get_object_or_404(Conduire,
                                         id_employe=request.POST.get('id_employe'),
                                         id_vehicule=request.POST.get('id_vehicule'),
                                         km_prise=request.POST.get('km_prise'),
                                         km_restit=None)
            restit_form = RestituerVehicule(request.POST, instance=conduire)

            if restit_form.is_valid():
                vehicule = Vehicule.objects.get(id=restit_form.cleaned_data['id_vehicule'].id)
                vehicule.km = restit_form.cleaned_data['km_restit']
                vehicule.save()
                restit_form.save()

                messages.success(request, 'Le véhicule à été réstitué avec succès.')
                return redirect('dashboard:index')

            # si le formulaire n'est pas valide
            else:
                messages.error(request, restit_form.errors)
                return redirect('dashboard:restituer_vehicule')

        # si le conducteur et véhicule n'ont pas encore étés selectionnés (donc requête GET)
        else:
            conduire = get_object_or_404(Conduire,
                                         id_employe=request.POST.get('recherche_cond'),
                                         id_vehicule=request.POST.get('recherche_veh'),
                                         date_et_temps_de_restitution=None,
                                         km_restit=None)
            context['restit_form'] = RestituerVehicule(instance=conduire,
                                                       initial={"date_et_temps_de_restitution": datetime.datetime.now()})

    context['restit_form_rechercher'] = RestituerVehiculeRecherche()
    context['liste_conducteurs_en_mission'] = Conduire.objects.filter(date_et_temps_de_prise__isnull=False,
                                                                      date_et_temps_de_restitution__isnull=True)
    return render(request=request,
                  template_name='dashboard/restituer.html',
                  context=context)


@login_required
def charger_vehicules(request):
    id_employe = request.GET.get('employe')
    conduites = Conduire.objects.filter(id_employe=id_employe,
                                        date_et_temps_de_restitution=None,
                                        km_restit=None)
    return render(request=request,
                  template_name='droplists/vehicules_dropdown_list_options.html',
                  context={'conduites': conduites})


@login_required
@user_passes_test(is_admin)
def ajouter_amende(request):
    if request.POST:
        ajouter_amende = AjouterAmende(request.POST)
        if ajouter_amende.is_valid():
            ajouter_amende.save()

            messages.success(request, "L'amende enregistrée avec succès.")
            return redirect('dashboard:index')

    context = updated_context()
    context['ajouter_amende_form'] = AjouterAmende()

    return render(request=request,
                  template_name='dashboard/ajout_amende.html',
                  context=context)


@login_required
@user_passes_test(is_admin)
def saisir_entretien(request):
    if request.POST:
        saisir_entretien = SaisirEntretien(request.POST)
        if saisir_entretien.is_valid():
            saisir_entretien.save()

            messages.success(request, "L'entretien à été saisi avec succès.")
            return redirect('dashboard:index')

    context = updated_context()
    context['saisir_entretien_form'] = SaisirEntretien()

    return render(request=request,
                  template_name='dashboard/saisir_entretien.html',
                  context=context)


@login_required
@user_passes_test(is_admin)
def msg(request):
    return render(request=request,
                  template_name='dashboard/msg.html',
                  context=updated_context())


@login_required
@user_passes_test(is_admin)
def voir_msg(request, pk):
    mess = MessageProbleme.objects.get(pk=pk)

    if mess.seen is False:
        mess.seen = True
        mess.save()

    context = updated_context()
    context['message'] = mess

    if request.POST:
        if request.POST.get('traite', False) == 'on':
            mess.solved = True
            mess.save()
            messages.success(request,
                             'Le message de ' + mess.id_employe.user.first_name + ' a été marqué comme traité')
        else:
            mess.solved = False
            mess.save()
            messages.error(request,
                           'Le message de ' + mess.id_employe.user.first_name + " n'a pas été marqué comme traité")

        return redirect('dashboard:msg')

    return render(request=request,
                  template_name='dashboard/voir_msg.html',
                  context=context)
