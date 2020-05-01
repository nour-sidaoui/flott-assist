from rest_framework import serializers

from employe.models import Conduire
from conducteur.models import MessageProbleme


class KmInSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conduire
        fields = ['km_prise',
                  'date_et_temps_de_prise',
                  ]


class KmOutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conduire
        fields = ['km_restit',
                  'date_et_temps_de_restitution',
                  ]


class MessageProblemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MessageProbleme
        fields = ['sent_at',
                  'sujet',
                  'text',
                  ]
