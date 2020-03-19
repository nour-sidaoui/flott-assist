from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from employe.views import updated_context


@login_required
def page_recherche(request):
    return render(request=request,
                  template_name='historique/page_recherche.html',
                  context=updated_context())


# @login_required
# def fiche_vehicule(request, pk):
#     vehicule = get_object_or_404(Vehicule, id=pk)
#
#     if request.POST:
#         veh_filled_form = ModifierVeh(request.POST, instance=vehicule)
#
#         if veh_filled_form.is_valid():
#             veh_filled_form.save()
#
#             messages.success(request, 'Véhicule modifié avec succès.')
#             return redirect('vehicule:page_vehicules')
#
#         else:
#             messages.error(request, veh_filled_form.errors)
#     else:
#         veh_filled_form = ModifierVeh(instance=vehicule)
#
#     context = updated_context()
#     context['veh_form_modifier'] = veh_filled_form
#
#     return render(request=request,
#                   template_name='vehicule/fiche.html',
#                   context=context)