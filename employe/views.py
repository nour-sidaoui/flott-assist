from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from django.shortcuts import render, redirect, get_object_or_404
from dashboard.views import updated_context, is_admin

from .models import Employe, Photo
from rest_framework.authtoken.models import Token

from .forms import (CreerUser,
                    ModifierUser,
                    CondForm,
                    PhotoForm
                    )


def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login/")


@login_required
@user_passes_test(is_admin)
def page_conducteurs(request):
    return render(request=request,
                  template_name='employe/conducteurs.html',
                  context=updated_context())


@login_required
@user_passes_test(is_admin)
def ajouter(request):
    # setting general template context
    context = updated_context()
    context['creer_user_form'] = CreerUser()
    context['creer_cond_form'] = CondForm()
    context['photo_form'] = PhotoForm()

    if request.method == 'POST':
        creer_user_form = CreerUser(request.POST)
        creer_cond_form = CondForm(request.POST)

        # Checking if both forms are valid
        if creer_user_form.is_valid() and creer_cond_form.is_valid():
            created_user_form = creer_user_form.save()
            created_cond_form = creer_cond_form.save(commit=False)
            created_cond_form.user = created_user_form

            # Creating token for added user
            Token.objects.create(user=created_user_form)

            # if picture file has been selected
            if len(request.FILES):
                photo_form = PhotoForm(request.POST, request.FILES)

                if photo_form.is_valid():
                    temp_photo_form = photo_form.save(commit=False)
                    created_cond_form.id_photo = temp_photo_form
                    photo_form.crop_and_save()

            created_cond_form.save()
            messages.success(request, 'Conducteur ajouté avec succès.')

            # adding picture messages "AFTER" main form messages
            if len(request.FILES):
                messages.success(request, 'Une photo de profil a également été ajoutée')
            else:
                messages.info(request, "Aucune photo n'a été ajoutée")

            return redirect('employe:page_conducteurs')

        # if errors in user_form and/or cond_form
        else:
            messages.error(request, creer_user_form.errors)
            messages.error(request, creer_cond_form.errors)

            # reassign the sent form to context (including errors)
            context['creer_user_form'] = creer_user_form
            context['creer_cond_form'] = creer_cond_form

    return render(request=request,
                  template_name='employe/ajouter.html',
                  context=context)


@login_required
@user_passes_test(is_admin)
def voir_profil(request, pk):
    conducteur = get_object_or_404(Employe, id=pk)
    user_filled_form = ModifierUser(instance=conducteur.user)
    cond_filled_form = CondForm(instance=conducteur)

    context = updated_context()
    context['user_form_modifier'] = user_filled_form
    context['cond_form_modifier'] = cond_filled_form
    context['photo_form'] = PhotoForm()
    context['conducteur'] = conducteur

    if request.POST:
        user_filled_form = ModifierUser(request.POST, instance=conducteur.user)
        cond_filled_form = CondForm(request.POST, instance=conducteur)

        if user_filled_form.is_valid() and cond_filled_form.is_valid():
            user = user_filled_form.save()
            cond = cond_filled_form.save(commit=False)
            cond.user = user

            # if picture file has been selected
            if len(request.FILES):

                # we find the old profile to delete it later (after new picture is saved)
                try:
                    old_profil_pic_id = conducteur.id_photo
                    old_profil_pic = Photo.objects.get(id=old_profil_pic_id.id)

                # do nothing in case there is no old picture
                except Photo.DoesNotExist:
                    pass

                # retrieving the submitted form
                photo_form = PhotoForm(request.POST, request.FILES, instance=conducteur.id_photo)

                if photo_form.is_valid():
                    temp_photo_form = photo_form.save(commit=False)
                    cond.id_photo = temp_photo_form
                    photo_form.crop_and_save()

                    # once new picture is saved, we delete the old picture
                    if old_profil_pic:
                        old_profil_pic.picture.delete(save=False)

            cond.save()

            messages.success(request, 'Conducteur modifié avec succès.')

            # adding picture messages "AFTER" main form messages
            if len(request.FILES):
                messages.success(request, 'La photo de profil a été mise à jour')
            else:
                messages.info(request, "Aucune modification n'a été enregistrée sur la photo")

            return redirect('employe:page_conducteurs')

        # if errors in user_filled_form and/or cond_filled_form
        else:
            messages.error(request, user_filled_form.errors)
            messages.error(request, cond_filled_form.errors)

            # reassign the sent form to context (including errors)
            context['user_form_modifier'] = user_filled_form
            context['cond_form_modifier'] = cond_filled_form

    # else if GET request
    return render(request=request,
                  template_name='employe/profil.html',
                  context=context)


# create token for shell created superuser

#   >>> from rest_framework.authtoken.models import Token
#   >>> from django.contrib.auth.models import User
#
#   >>> usr = User.objects.get(username='admin')
#   >>> Token.objects.create(user=usr)

