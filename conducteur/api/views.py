from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from conducteur.models import MessageProbleme
from employe.models import Employe, Conduire

from dashboard.views import report_difference
from datetime import datetime

from django.http import JsonResponse
from conducteur.api.serializers import (KmInSerializer,
                                        KmOutSerializer,
                                        MessageProblemeSerializer,
                                        GpsSerializer)


def debug_print(m):
    print('\n********' * 3)
    print('\t\t\t' + str(m))
    print('********\n' * 3)


def retrieve_employe(request):
    """retrieves Employe object from request"""
    full_token = request.META.get('HTTP_AUTHORIZATION')             # gets 'Token 634F2D356...'
    token = Token.objects.get(key=full_token.split()[1])            # isolating token number only
    return Employe.objects.get(user_id=token.user_id)               # return sender's Employe object


@api_view(['POST', 'GET'])
@permission_classes((IsAuthenticated,))
def api_km_prise(request):
    """POST saved entered Km and GET returns Km and date_de_prise """

    conducteur = retrieve_employe(request)                          # retrieving sender's Employe object

    # using with transaction.atomic() to lock the db row with select_for_update() on the entire block
    with transaction.atomic():

        try:
            conduite = Conduire.objects.select_for_update().get(id_employe=conducteur,
                                                                km_restit=None)

        except Conduire.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # TypeError exception raises in case of concurrency as the object will not be callable
        except TypeError:
            return Response(status=status.HTTP_409_CONFLICT)

        if request.method == 'POST':
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
    """receives and saves km_de_restit and adds actual time"""
    conducteur = retrieve_employe(request)                          # retrieving sender's Employe object

    # using with transaction.atomic() to lock the db row with select_for_update() on the entire block
    with transaction.atomic():
        try:
            conduite = Conduire.objects.select_for_update().get(id_employe=conducteur,
                                                                km_restit=None)
        except Conduire.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # TypeError exception raises in case of concurrency as the object will not be callable
        except TypeError:
            return Response(status=status.HTTP_409_CONFLICT)

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
                                             id_vehicule=conduite.id_vehicule,
                                             solved=False).exclude(sujet='Coord. GPS partagées').latest('sent_at')

    except (Conduire.DoesNotExist, MessageProbleme.DoesNotExist):
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = MessageProblemeSerializer(msg)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes((IsAuthenticated,))
def api_get_veh(request):
    """returns assigned vehicle's plate number"""
    conducteur = retrieve_employe(request)                          # retrieving sender's Employe object

    try:
        conduite = Conduire.objects.get(id_employe=conducteur,
                                        km_restit=None)

    except Conduire.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = {'veh_immat': conduite.id_vehicule.immat}

    return JsonResponse(data)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_declarer_prob(request):
    """receives a declared problem to conduite instance"""
    conducteur = retrieve_employe(request)                          # retrieving sender's Employe object

    # using with transaction.atomic() to lock the db row with select_for_update() on the entire block
    with transaction.atomic():
        try:
            conduite = Conduire.objects.select_for_update().get(id_employe=conducteur,
                                                                km_restit=None)

        except Conduire.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # TypeError exception raises in case of concurrency as the object will not be callable
        except TypeError:
            return Response(status=status.HTTP_409_CONFLICT)

        msg = MessageProbleme(id_employe=conducteur,
                              id_vehicule=conduite.id_vehicule)

        serializer = MessageProblemeSerializer(msg, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST', ])
@permission_classes((IsAuthenticated,))
def api_gps(request):
    """receives GPS coordinates from mobile app"""
    conducteur = retrieve_employe(request)                          # retrieving sender's Employe object

    # using with transaction.atomic() to lock the db row with select_for_update() on the entire block
    with transaction.atomic():
        try:
            conduite = Conduire.objects.select_for_update().get(id_employe=conducteur,
                                                                km_restit=None)

        except Conduire.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # TypeError exception raises in case of concurrency as the object will not be callable
        except TypeError:
            return Response(status=status.HTTP_409_CONFLICT)

        msg = MessageProbleme(id_employe=conducteur,
                              id_vehicule=conduite.id_vehicule,
                              sujet='Coord. GPS partagées')

        serializer = GpsSerializer(msg, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT', ])
@permission_classes((IsAuthenticated,))
def api_modifer_prob(request):
    """modifies last message"""
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

