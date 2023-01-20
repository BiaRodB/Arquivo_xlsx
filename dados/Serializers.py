from rest_framework import serializers
from dados.models import Inserir
import pandas as pd


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inserir
        fields = '__all__'
        