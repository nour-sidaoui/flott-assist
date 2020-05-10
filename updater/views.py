from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from git import Repo


@csrf_exempt
def update(request):
    if request.method == "POST":
        repo = Repo("flott-assist/")
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")
