from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import git


@csrf_exempt
def update(request):
    import sys
    print('\n'.join(sys.path))

    if request.method == "POST":
        '''
        pass the path of the diectory where your project will be 
        stored on PythonAnywhere in the git.Repo() as parameter.
        Here the name of my directory is "test.pythonanywhere.com"
        '''

        repo = git.Repo("sidaoui.pythonanywhere.com/")
        origin = repo.remotes.origin

        origin.pull()

        return HttpResponse("Updated code on PythonAnywhere")
    else:
        return HttpResponse("Couldn't update the code on PythonAnywhere")
