from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required

from employe.views import updated_context
from employe.models import Employe, Conduire, Amende
from vehicule.models import Vehicule, Entretien

from django.db.models import Sum


@login_required
def page_recherche(request):
    context = updated_context()

    if request.POST:
        if request.POST.get('recherche_cond') != '0':
            context['recherche_cond'] = True

            # retrieve selected employe and add it to context
            employe_selectionne = Employe.objects.get(pk=request.POST.get('recherche_cond'))
            context['cond_selectionne'] = employe_selectionne

            # retrieve instances of Conduire
            conduites = Conduire.objects.filter(id_employe=employe_selectionne)
            context['conduites'] = conduites

            # retrieve fines linked to employe_selectionné
            amendes = Amende.objects.filter(id_employe=employe_selectionne)
            context['amendes'] = amendes

            # retrieve the sum of amendes
            total_amendes = amendes.aggregate(sum=Sum('montant'))['sum']
            context['total_amendes'] = total_amendes

        if request.POST.get('recherche_veh') != '0':
            context['recherche_veh'] = True

            # retrieve selected vehicule and add it to context
            vehicule_selectionne = Vehicule.objects.get(pk=request.POST.get('recherche_veh'))
            context['veh_selectionne'] = vehicule_selectionne


            # retrieve the sum of amendes
            amendes = Amende.objects.filter(id_vehicule=vehicule_selectionne)
            context['amendes'] = amendes

            # retrieve the sum of amendes
            total_amendes = amendes.aggregate(sum=Sum('montant'))['sum']
            context['total_amendes'] = total_amendes

            # retrieve sum of vehicule services
            frais_d_entretien = Entretien.objects.filter(id_vehicule=vehicule_selectionne)
            total_frais_d_entretien = frais_d_entretien.aggregate(sum=Sum('montant'))['sum']
            context['total_frais_d_entretien'] = total_frais_d_entretien

            # retrieve most recent service date if any
            entretiens = Entretien.objects.filter(id_vehicule=vehicule_selectionne)
            context['entretiens'] = entretiens

            # retrieve most recent service date if any
            if entretiens:
                dernier_entretien = entretiens.latest('date')
                context['dernier_entretien'] = dernier_entretien

            # retrieve instances of Conduire
            conduites = Conduire.objects.filter(id_vehicule=vehicule_selectionne)
            context['conduites'] = conduites

    return render(request=request,
                  template_name='historique/page_recherche.html',
                  context=context)


