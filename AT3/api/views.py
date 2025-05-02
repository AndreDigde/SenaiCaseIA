from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .constants import *
from . import serializers, models
from datetime import datetime

# Create your views here.
class AuthView(APIView):
    @swagger_auto_schema(operation_summary='Authenticate a User',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                USERNAME_LABEL: openapi.Schema(type=openapi.TYPE_STRING, description='User username', example='admin'),
                PASSWORD_LABEL: openapi.Schema(type=openapi.TYPE_STRING, description='User password', example='Senai@2025'),
                }),
        responses={
                status.HTTP_200_OK: 'Authorization token',
                status.HTTP_400_BAD_REQUEST: 'Invalid credentials json data',
            })
    def post(self, request):
        try:
            user_username = request.data[USERNAME_LABEL]
            user_password = request.data[PASSWORD_LABEL]
            user = models.User.objects.get(username=user_username, password=user_password)
        except Exception:
            return Response({'message': 'invalid credentials!'}, status=400)
        refresh = RefreshToken.for_user(user)
        return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=200)


class PredictionView(APIView):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary='GET a Prediction by Id',
        responses={
            status.HTTP_200_OK: 'Returns the prediction',
            status.HTTP_404_NOT_FOUND: 'Prediction not found',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
        },
        manual_parameters=[
            openapi.Parameter(name=PREDICTION_ID_LABEL,
                type=openapi.TYPE_INTEGER,
                description='The id of prediction',
                required=True,
                in_=openapi.IN_PATH,
                example=1,
            )])
    def get(self, request, prediction_id):
        try:
            prediction = models.Prediction.objects.get(prediction_id=prediction_id)
        except Exception:
            return Response({'message': 'prediction not found!'}, status=404)
        prediction_serializer = serializers.PredictionSerializer(prediction)
        return Response(prediction_serializer.data, status=200)
    

class PerformPredictionView(APIView):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary='POST a Prediction',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                RELATIVE_COMPACTNESS_LABEL: openapi.Schema(type=openapi.TYPE_NUMBER, description='Relative Compactness', example=0.79),
                SURFACE_AREA_LABEL: openapi.Schema(type=openapi.TYPE_NUMBER, description='Surface Area', example=637.0),
                WALL_AREA_LABEL: openapi.Schema(type=openapi.TYPE_NUMBER, description='Wall Area', example=343.0),
                ROOF_AREA_LABEL: openapi.Schema(type=openapi.TYPE_NUMBER, description='Roof Area', example=147.0),
                OVERALL_HEIGHT_LABEL: openapi.Schema(type=openapi.TYPE_NUMBER, description='Overall Height', example=7.0),
                ORIENTATION_LABEL: openapi.Schema(type=openapi.TYPE_INTEGER, description='Orientation', example=3),
                GLAZING_AREA_LABEL: openapi.Schema(type=openapi.TYPE_NUMBER, description='Glazing Area', example=0.0),
                }),
        responses={
                status.HTTP_200_OK: 'Prediction saved',
                status.HTTP_400_BAD_REQUEST: 'Invalid prediction json data',
                status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
            })
    def post(self, request):
        prediction_serializer = serializers.PredictionSerializer(data=request.data)
        if prediction_serializer.is_valid():
            data = dict(prediction_serializer.validated_data)
            data['heating_load'] = 10.5
            data['colding_load'] = 10.5
            prediction = models.Prediction(**data)
            prediction.save()
            prediction_serializer = serializers.PredictionSerializer(prediction)
            return Response(prediction_serializer.data, status=200)
        return Response({'message': 'invalid prediction json data!'}, status=400)

class ListPredictionView(APIView):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary='List Predictions in a datetime interval',
        responses={
            status.HTTP_200_OK: 'Returns the list of predictions',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
        },
        manual_parameters=[
            openapi.Parameter(name=RELATIVE_COMPACTNESS_LABEL, in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=False),
            openapi.Parameter(name=SURFACE_AREA_LABEL, in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=False),
            openapi.Parameter(name=WALL_AREA_LABEL, in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=False),
            openapi.Parameter(name=ROOF_AREA_LABEL, in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=False),
            openapi.Parameter(name=OVERALL_HEIGHT_LABEL, in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=False),
            openapi.Parameter(name=ORIENTATION_LABEL, in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter(name=GLAZING_AREA_LABEL, in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=False),
            openapi.Parameter(name=HEATING_LOAD_LABEL, in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=False),
            openapi.Parameter(name=COLDING_LOAD_LABEL, in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=False),
            ])
    def get(self, request):
        filters = {}
        query_params = request.query_params

        filter_fields = [ RELATIVE_COMPACTNESS_LABEL, SURFACE_AREA_LABEL, WALL_AREA_LABEL, ROOF_AREA_LABEL, OVERALL_HEIGHT_LABEL,
                            ORIENTATION_LABEL, GLAZING_AREA_LABEL, HEATING_LOAD_LABEL, COLDING_LOAD_LABEL,]

        for field in filter_fields:
            value = query_params.get(field)
            if value is not None:
                filters[field] = value

        predictions = models.Prediction.objects.filter(**filters)
        predictions_serializer = serializers.PredictionSerializer(predictions, many=True)
        predictions_list = list(predictions_serializer.data)
        return Response({'predictions': predictions_list, 'total': len(predictions_list)}, status=200)
