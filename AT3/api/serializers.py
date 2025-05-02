from rest_framework import serializers
from . import models

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Prediction
        fields = '__all__'
        read_only_fields = ['heating_load', 'colding_load']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'password')
