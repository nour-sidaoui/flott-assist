from django.shortcuts import render, redirect

from dashboard.views import report_difference
from employe.models import Conduire
from vehicule.models import Vehicule

from .models import MessageProbleme
from .forms import FormConduirePrise, FormConduireRestit, FormMessage

from django.contrib import messages


def index(request):
    return render(request=request,
                  template_name='conducteur/index.html',
                  context=None)


def page_km_in(request):
    try:
        conduite = Conduire.objects.get(id_employe=request.user.employe.id, km_restit=None)

    except Conduire.DoesNotExist:
        messages.error(request, 'Aucun véhicule ne vous a été attribué')
        return redirect('conducteur:index')

    form_conduite = FormConduirePrise(instance=conduite)

    context = {'conduite': conduite,
               'form_conduite': form_conduite,
               }

    # gathering vehicle's issues
    issues = MessageProbleme.objects.filter(id_vehicule=conduite.id_vehicule,
                                            solved=False)
    if issues:
        issue = issues.latest('sent_at')
        context['issue'] = issue

    if request.POST:
        form_conduite = FormConduirePrise(request.POST, instance=conduite)

        if form_conduite.is_valid():
            # vehicule = Vehicule.objects.get(id=conduite.id_vehicule.id)
            # vehicule.km = form_conduite.cleaned_data['km_prise']
            # vehicule.save()

            # raising a notification in case of discrepancy
            if form_conduite.cleaned_data['km_prise'] != conduite.id_vehicule.km:

                difference = form_conduite.cleaned_data['km_prise']

                # calling the function that raises a notification
                report_difference(conduite.id_employe, conduite.id_vehicule, difference)

            form_conduite.save()
            messages.success(request, 'Km de prise a été enregistré avec succès')
            return redirect('conducteur:index')

        else:
            messages.error(request, form_conduite.errors)
            return redirect()

    return render(request=request,
                  template_name='conducteur/km_in.html',
                  context=context)


def page_km_out(request):
    try:
        conduite = Conduire.objects.get(id_employe=request.user.employe.id, km_restit=None)

    except Conduire.DoesNotExist:
        messages.error(request, "Vous n'avez aucun véhicule à restituer")
        return redirect('conducteur:index')

    form_conduite = FormConduireRestit(instance=conduite)

    context = {'conduite': conduite,
               'form_conduite': form_conduite}

    if request.POST:
        form_conduite = FormConduireRestit(request.POST, instance=conduite)

        if form_conduite.is_valid():
            vehicule = Vehicule.objects.get(id=conduite.id_vehicule.id)
            vehicule.km = form_conduite.cleaned_data['km_restit']
            vehicule.save()

            form_conduite.save()
            messages.success(request, 'Le vehicule ' + conduite.id_vehicule.immat + ' a été restitué avec succès')
            return redirect('conducteur:index')

        else:
            messages.error(request, form_conduite.errors)
            return redirect()

    return render(request=request,
                  template_name='conducteur/km_out.html',
                  context=context)


def declarer_prob(request):
    try:
        conduite = Conduire.objects.get(id_employe=request.user.employe.id,
                                        km_restit=None)

    except Conduire.DoesNotExist:
        messages.error(request, "Un véhicule doit vous être attribué pour déclarer un problème.")
        return redirect('conducteur:index')

    form_message = FormMessage()

    context = {'conduite': conduite,
               'form_message': form_message}

    if request.POST:
        filled_form_message = FormMessage(request.POST, instance=MessageProbleme(
            id_employe=request.user.employe,
            id_vehicule=conduite.id_vehicule
        ))

        if filled_form_message.is_valid():
            filled_form_message.save()

            messages.success(request, 'Votre message a été envoyé avec succès.')
            return redirect('conducteur:index')

        else:
            messages.error(request, filled_form_message.errors)
            return redirect()

    return render(request=request,
                  template_name='conducteur/declarer_prob.html',
                  context=context)


def contacter_assist(request):
    return render(request=request,
                  template_name='conducteur/contacter_assist.html',
                  context=None)
