from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, F

from .models import Notification
from vehicule.models import Vehicule
from employe.models import Employe, Conduire
from conducteur.models import MessageProbleme

import datetime

from .forms import (AttribuerVehicule,
                    RestituerVehiculeRecherche,
                    RestituerVehicule,
                    AjouterAmende,
                    SaisirEntretien,
                    )


def notification_factory():
    upcoming_month = datetime.date.today() + datetime.timedelta(days=30)
    two_weeks_expiry = datetime.date.today() + datetime.timedelta(days=14)

    # generating notifications for new technical_inspections (if any)
    vehicules_a_controler = Vehicule.objects.filter(prochain_controle_technique__lte=upcoming_month,
                                                    disponible=True)
    if vehicules_a_controler:
        for vehicule_a_controler in vehicules_a_controler:
            vac = Notification(id_vehicule=vehicule_a_controler,
                               is_ct=True)

            if Notification.objects.filter(created_on__lte=two_weeks_expiry,
                                           id_vehicule=vehicule_a_controler,
                                           is_ct=vac.is_ct,
                                           is_entretien=vac.is_entretien,
                                           is_assurance=vac.is_assurance).count() < 1:
                vac.save()

    # generating notifications for new upcoming services (if any)
    vehicules_a_entretenir = Vehicule.objects.filter(Q(prochain_entretien_date__lte=upcoming_month) |
                                                     Q(prochain_entretien_km__lte=(F('km') + 1000)),
                                                     disponible=True)
    if vehicules_a_entretenir:
        for vehicule_a_entretenir in vehicules_a_entretenir:
            vae = Notification(id_vehicule=vehicule_a_entretenir,
                               is_entretien=True)

            if Notification.objects.filter(created_on__lte=two_weeks_expiry,
                                           id_vehicule=vehicule_a_entretenir,
                                           is_entretien=True).count() < 1:
                vae.save()

    # generating notifications for new upcoming insurance renewals (if any)
    vehicules_a_assurer = Vehicule.objects.filter(validite_assurance__lte=upcoming_month,
                                                  disponible=True)

    if vehicules_a_assurer:
        for vehicule_a_assurer in vehicules_a_assurer:
            vaa = Notification(id_vehicule=vehicule_a_assurer,
                               is_assurance=True)

            if Notification.objects.filter(created_on__lte=two_weeks_expiry,
                                           id_vehicule=vehicule_a_assurer,
                                           is_assurance=True).count() < 1:
                vaa.save()


def get_notifications():
    notification_factory()
    return Notification.objects.filter(seen=False).order_by('-created_on')


def report_difference(driver, vehicle, reported_km):
    sujet = "Diff. de km détectée"
    text = f"Une différence de {reported_km - vehicle.km} Km à été détectée." \
           f"\n\nDernier Km de restitution : {vehicle.km} Km." \
           f"\n\nKm de prise signalé par {driver} à la prise: {reported_km}"

    msg_de_notif = MessageProbleme(id_vehicule=vehicle,
                                   sujet=sujet,
                                   text=text)
    msg_de_notif.save()


def updated_context():
    """Remets à jour le dictionnaire contexte et le 'return' """
    notifications = get_notifications()

    liste_messages_non_lus = MessageProbleme.objects.filter(seen=False).order_by('-sent_at')
    liste_messages_lus = MessageProbleme.objects.filter(seen=True).order_by('-sent_at')

    liste_vehicules = Vehicule.objects.all().order_by('marque')
    liste_vehicules_disponibles = Vehicule.objects.filter(disponible=True)

    liste_conducteurs = sorted(Employe.objects.all(), key=lambda m: m.user.first_name.lower())
    liste_conducteurs_presents = sorted(Employe.objects.filter(Q(date_de_fin__gt=datetime.datetime.now()) |
                                                               Q(date_de_fin=None)),
                                        key=lambda m: m.user.first_name.lower())

    context = {'notifications': notifications,

               'liste_messages_non_lus': liste_messages_non_lus,
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

    # retrieving and filtering events in the next 30 days or 1000km and merging them in sorted events
    upcoming_month = datetime.date.today() + datetime.timedelta(days=30)
    liste_controles_tech = Vehicule.objects.filter(prochain_controle_technique__lte=upcoming_month)

    liste_entretiens = Vehicule.objects.filter(Q(prochain_entretien_date__lte=upcoming_month) |
                                               Q(prochain_entretien_km__lte=(F('km') + 1000)))

    events = liste_controles_tech | liste_entretiens
    sorted_events = events.order_by('prochain_entretien_km',
                                    'prochain_controle_technique',
                                    'prochain_entretien_date')

    # gathering messages marked as unresolved
    unresolved_msgs = sorted(MessageProbleme.objects.filter(solved=False), key=lambda m: m.sent_at, reverse=True)

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
    context['sorted_events'] = sorted_events
    context['conduites'] = conduites
    context['unresolved_msgs'] = unresolved_msgs
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

        else:
            # si le conducteur et véhicule n'ont pas encore étés selectionnés (donc requête GET)
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

    print('\n\n\n\n\n\n')
    print(conduites)
    print('\n\n\n\n\n\n')

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
            messages.success(request, "Le message de a été marqué comme traité")
        else:
            mess.solved = False
            mess.save()
            messages.error(request, "Le message de a pas été marqué comme non-traité")

        return redirect('dashboard:msg')

    return render(request=request,
                  template_name='dashboard/voir_msg.html',
                  context=context)
