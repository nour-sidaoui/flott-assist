from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from conducteur.models import MessageProbleme
from employe.models import Employe, Conduire

from dashboard.views import report_difference
from datetime import datetime

from conducteur.api.serializers import (KmInSerializer,
                                        KmOutSerializer,
                                        MessageProblemeSerializer)


def debug_print(m):
    print('\n********' * 3)
    print('\t\t\t' + str(m))
    print('********\n' * 3)


def retrieve_employe(request):
    """retrieves Employe object from request"""
    full_token = request.META.get('HTTP_AUTHORIZATION')             # gets 'Token 634F2D356...'
    token = Token.objects.get(key=full_token.split()[1])            # isolating token number only
    return Employe.objects.get(user_id=token.user_id)               # return sender's Employe object


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
def api_km_prise(request):
    conducteur = retrieve_employe(request)                          # retrieving sender's Employe object

    try:
        conduite = Conduire.objects.get(id_employe=conducteur,
                                        km_prise=None,
                                        km_restit=None)
    except Conduire.DoesNotExist:
        debug_print('conduire does not exist')
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.POST:
        serializer = KmInSerializer(conduite, data=request.data)

        if serializer.is_valid():
            vehicule = conduite.id_vehicule

            # creating notification and message if Km does not match
            if vehicule.km != serializer.validated_data['km_prise']:

                difference = serializer.validated_data['km_prise']

                # calling the function that raises a notification
                report_difference(conducteur, vehicule, difference)

                vehicule.km = serializer.validated_data['km_prise']
                vehicule.save()

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # else if request is GET
    serializer = KmInSerializer(conduite)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_km_restit(request):
    conducteur = retrieve_employe(request)                          # retrieving sender's Employe object

    try:
        conduite = Conduire.objects.get(id_employe=conducteur,
                                        km_restit=None)
    except Conduire.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    conduite.date_et_temps_de_restitution = datetime.now()
    conduite.save()

    serializer = KmOutSerializer(conduite, data=request.data)

    if serializer.is_valid():
        vehicule = conduite.id_vehicule
        vehicule.km = serializer.validated_data['km_restit']
        vehicule.save()

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_voir_prob(request):
    conducteur = retrieve_employe(request)                          # retrieving sender's Employe object

    try:
        conduite = Conduire.objects.get(id_employe=conducteur,
                                        km_restit=None)

        msg = MessageProbleme.objects.filter(id_employe=conducteur,
                                             id_vehicule=conduite.id_vehicule).latest('sent_at')

    except (Conduire.DoesNotExist, MessageProbleme.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MessageProblemeSerializer(msg)
    return Response(serializer.data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_declarer_prob(request):
    conducteur = retrieve_employe(request)                          # retrieving sender's Employe object

    try:
        conduite = Conduire.objects.get(id_employe=conducteur,
                                        km_restit=None)

    except Conduire.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    msg = MessageProbleme(id_employe=conducteur,
                          id_vehicule=conduite.id_vehicule)

    serializer = MessageProblemeSerializer(msg, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_modifer_prob(request):
    conducteur = retrieve_employe(request)                          # retrieving sender's Employe object

    try:
        conduite = Conduire.objects.get(id_employe=conducteur,
                                        km_restit=None)

        msg = MessageProbleme.objects.filter(id_employe=conducteur,
                                             id_vehicule=conduite.id_vehicule).latest('sent_at')

    except (Conduire.DoesNotExist, MessageProbleme.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MessageProblemeSerializer(msg, data=request.data)
    data = {}

    if serializer.is_valid():
        serializer.save()
        data['success'] = "Le message à été modifié avec succès."
        return Response(data=data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

