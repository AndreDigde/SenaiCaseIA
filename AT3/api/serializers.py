from rest_framework import serializers
from . import models

class PredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Prediction
        fields = '__all__'
        read_only_fields = ['heating_load', 'colding_load']


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = models.User
        fields = ['id', 'email', 'full_name', 'phone', 'password']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = models.User(**validated_data)
        user.username = user.email
        user.set_password(password)
        user.save()
        return user


class UserReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'email', 'full_name', 'phone']
