from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponseRedirect, HttpResponse

from .models import Employe, Conduire, Amende
from .forms import AjouterCond
from vehicule.models import Vehicule
from django.contrib import messages
from datetime import datetime
from django.db.models import Q


def reformat_date(d):
    """ nettoye les '\Xa0' autour des dates et les retransforme en objets datetime """
    if d != '':
        d.replace(u'\xa0', ' ')
        date = datetime.strptime(d, '%Y-%m-%d')
        return date.strftime('%Y-%m-%d')
    return None


def updated_context():
    """Remets à jour le dictionnaire contexte et le 'return' """
    liste_vehicules = Vehicule.objects.all()
    liste_admin = Employe.objects.filter(admin=True)
    liste_conducteurs = Employe.objects.filter(admin=False)
    liste_conducteurs_presents = Employe.objects.filter(admin=False)\
                                                .filter(Q(date_de_fin__gt=datetime.now()) | Q(date_de_fin=None))

    context = {'liste_vehicules': liste_vehicules,
               'liste_admin': liste_admin,
               'liste_conducteurs': liste_conducteurs,
               'liste_conducteurs_presents': liste_conducteurs_presents,
               'num_employe': Employe.num_employe,
               'form': AjouterCond,
               }
    return context


def index(request):
    return render(request, 'employe/index.html', updated_context())


def page_conducteurs(request):
    return render(request, 'employe/conducteurs.html', updated_context())


def ajouter(request):
    if request.method == 'POST':
        form = AjouterCond(request.POST)
        if form.is_valid():

            cond = Employe(num_employe=form.cleaned_data['num_employe'],
                           nom=form.cleaned_data['nom'],
                           prenom=form.cleaned_data['prenom'],
                           tel=form.cleaned_data['tel'],
                           adresse=form.cleaned_data['adresse'],
                           email=form.cleaned_data['email'],
                           admin=False,
                           num_permis=form.cleaned_data['num_permis'],
                           date_de_debut=form.cleaned_data['date_de_debut'],
                           date_de_fin=form.cleaned_data['date_de_fin']
                           )
            cond.save()
            messages.success(request, 'Conducteur ajouté avec succès.')
            return redirect('employe:page_conducteurs')

        else:
            messages.error(request, form.errors)
            return HttpResponseRedirect('ajouter')

    return render(request, 'employe/ajouter.html', updated_context())


def voir_profil(request, pk):
    conducteur = get_object_or_404(Employe, num_employe=pk)
    filled_form = AjouterCond(request.POST or None, instance=conducteur)

    if request.method == "POST":
        filled_form = AjouterCond(request.POST, instance=conducteur)

        if filled_form.is_valid():
            conducteur.nom = filled_form['nom'].value()
            conducteur.prenom = filled_form['prenom'].value()
            conducteur.tel = filled_form['tel'].value()
            conducteur.adresse = filled_form['adresse'].value()
            conducteur.email = filled_form['email'].value()
            conducteur.num_permis = filled_form['num_permis'].value()

            # on utilise la fonction reformat_date pour nettoyer l'input du formulaire et le return en objet datetime
            conducteur.date_de_debut = reformat_date(filled_form['date_de_debut'].value())
            conducteur.date_de_fin = reformat_date(filled_form['date_de_fin'].value())

            conducteur.save()

            messages.success(request, 'Conducteur modifié avec succès.')
            return redirect('employe:voir_profil', pk=pk)

        else:
            messages.error(request, filled_form.errors)
            context = updated_context()
            context['formulaire'] = filled_form

    context = updated_context()
    context['formulaire'] = filled_form
    return render(request, 'employe/profil.html', context)
