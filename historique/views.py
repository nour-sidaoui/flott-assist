from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from employe.views import updated_context


@login_required
def page_recherche(request):
    return render(request=request,
                  template_name='historique/page_recherche.html',
                  context=updated_context())
