from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .constants import *
from . import serializers, models, regressor

# Create your views here.
class AuthView(APIView):
    @swagger_auto_schema(operation_summary='Authenticate a User',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                USER_EMAIL_LABEL: openapi.Schema(type=openapi.TYPE_STRING, description='User email', example='mail@mail.com'),
                USER_PASS_LABEL: openapi.Schema(type=openapi.TYPE_STRING, description='User password', example='umasenha'),
            }),
        responses={
                status.HTTP_200_OK: 'Authorization token',
                status.HTTP_400_BAD_REQUEST: 'Invalid credentials json data',
            })
    def post(self, request):
        try:
            user_email = request.data.get(USER_EMAIL_LABEL)
            user_password = request.data.get(USER_PASS_LABEL)
            user = authenticate(request, username=user_email, password=user_password)
            if user is None:
                return Response({'message': 'Invalid credentials!'}, status=status.HTTP_400_BAD_REQUEST)

            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'message': 'Invalid request!', 'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='Get user by Id',
        responses={
            status.HTTP_200_OK: 'Returns the user',
            status.HTTP_404_NOT_FOUND: 'User not found',
        },
        manual_parameters=[
            openapi.Parameter(
                name=USER_ID_LABEL,
                type=openapi.TYPE_INTEGER,
                in_=openapi.IN_PATH,
                required=True,
                description='The Id of the user'
            )])
    def get(self, request, user_id):
        try:
            user = models.User.objects.get(id=user_id)
        except Exception:
            return Response({'message': 'User not found!'}, status=404)
        serializer = serializers.UserReadSerializer(user)
        return Response(serializer.data, status=200)

    @swagger_auto_schema(
        operation_summary='Update a user by Id',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                USER_EMAIL_LABEL: openapi.Schema(type=openapi.TYPE_STRING, format='email', description='E-mail address used for login', example='user@example.com'),
                USER_NAME_LABEL: openapi.Schema(type=openapi.TYPE_STRING, description='Full name of the user', example='Um User'),
                USER_PASS_LABEL: openapi.Schema(type=openapi.TYPE_STRING, description='User password', example='umasenha'),
                USER_PHONE_LABEL: openapi.Schema(type=openapi.TYPE_STRING, description='Phone number of the user', example='(99) 99999-9999'),
            }
        ),
        responses={
            status.HTTP_200_OK: 'User updated successfully',
            status.HTTP_400_BAD_REQUEST: 'Invalid user json data',
            status.HTTP_404_NOT_FOUND: 'User not found',
        })
    def put(self, request, user_id):
        try:
            user = models.User.objects.get(id=user_id)
        except Exception:
            return Response({'message': 'User not found!'}, status=404)
        user_serializer = serializers.UserSerializer(user, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(status=200)
        return Response({'message': 'invalid user json data!'}, status=400)

    @swagger_auto_schema(
        operation_summary='Delete a user by Id',
        responses={
            status.HTTP_200_OK: 'User deleted successfully',
            status.HTTP_404_NOT_FOUND: 'User not found',
        }
    )
    def delete(self, request, user_id):
        try:
            user = models.User.objects.get(id=user_id)
        except Exception:
            return Response({'message': 'User not found!'}, status=404)
        user.delete()
        return Response(status=200)


class CreateUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary='Create a new user',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[USER_EMAIL_LABEL, USER_NAME_LABEL, USER_PASS_LABEL, USER_PHONE_LABEL],
            properties={
                USER_EMAIL_LABEL: openapi.Schema(type=openapi.TYPE_STRING, format='email', description='E-mail address used for login', example='user@example.com'),
                USER_NAME_LABEL: openapi.Schema(type=openapi.TYPE_STRING, description='Full name of the user', example='Um User'),
                USER_PASS_LABEL: openapi.Schema(type=openapi.TYPE_STRING, description='User password', example='umasenha'),
                USER_PHONE_LABEL: openapi.Schema(type=openapi.TYPE_STRING, description='Phone number of the user', example='(99) 99999-9999'),
            }
        ),
        responses={
            status.HTTP_201_CREATED: 'User created successfully',
            status.HTTP_400_BAD_REQUEST: 'Invalid data',
        })
    def post(self, request):
        user_serializer = serializers.UserSerializer(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(status=201)
        return Response({'message': 'Invalid user json data!'}, status=400)


class PredictionView(APIView):
    permission_classes = [IsAuthenticated]

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
    
    @swagger_auto_schema(operation_summary='DELETE a Prediction by Id',
        responses={
            status.HTTP_200_OK: 'Prediction deleted successfully',
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
    def delete(self, request, prediction_id):
        try:
            prediction = models.Prediction.objects.get(prediction_id=prediction_id)
        except Exception:
            return Response({'message': 'prediction not found!'}, status=404)
        prediction.delete()
        return Response(status=200)


class ListUserView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary='List Users with optional filters',
        responses={
            status.HTTP_200_OK: 'Returns the list of users',
            status.HTTP_401_UNAUTHORIZED: 'Unauthorized',
        },
        manual_parameters=[
            openapi.Parameter(name=USER_EMAIL_LABEL, in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter(name=USER_NAME_LABEL, in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
            openapi.Parameter(name=USER_PHONE_LABEL, in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, required=False),
        ])
    def get(self, request):
        filters = {}
        query_params = request.query_params
        filter_fields = [USER_EMAIL_LABEL, USER_NAME_LABEL, USER_PHONE_LABEL]
        for field in filter_fields:
            value = query_params.get(field)
            if value is not None:
                filters[field] = value

        users = models.User.objects.filter(**filters)
        users_serializer = serializers.UserReadSerializer(users, many=True)
        users_list = list(users_serializer.data)
        return Response({'users': users_list, 'total': len(users_list)}, status=200)


class PerformPredictionView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary='POST a Prediction',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[RELATIVE_COMPACTNESS_LABEL, SURFACE_AREA_LABEL, WALL_AREA_LABEL, ROOF_AREA_LABEL,
                        OVERALL_HEIGHT_LABEL, ORIENTATION_LABEL, GLAZING_AREA_LABEL, GLAZING_AREA__DIST_LABEL],
            properties={
                RELATIVE_COMPACTNESS_LABEL: openapi.Schema(type=openapi.TYPE_NUMBER, description='Relative Compactness', example=0.79),
                SURFACE_AREA_LABEL: openapi.Schema(type=openapi.TYPE_NUMBER, description='Surface Area', example=637.0),
                WALL_AREA_LABEL: openapi.Schema(type=openapi.TYPE_NUMBER, description='Wall Area', example=343.0),
                ROOF_AREA_LABEL: openapi.Schema(type=openapi.TYPE_NUMBER, description='Roof Area', example=147.0),
                OVERALL_HEIGHT_LABEL: openapi.Schema(type=openapi.TYPE_NUMBER, description='Overall Height', example=7.0),
                ORIENTATION_LABEL: openapi.Schema(type=openapi.TYPE_INTEGER, description='Orientation', example=3),
                GLAZING_AREA_LABEL: openapi.Schema(type=openapi.TYPE_NUMBER, description='Glazing Area', example=0.0),
                GLAZING_AREA__DIST_LABEL: openapi.Schema(type=openapi.TYPE_INTEGER, description='Glazing Area Distribution', example=0),
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

            features_key = [RELATIVE_COMPACTNESS_LABEL, SURFACE_AREA_LABEL, WALL_AREA_LABEL, ROOF_AREA_LABEL, OVERALL_HEIGHT_LABEL,
                                ORIENTATION_LABEL, GLAZING_AREA_LABEL, GLAZING_AREA__DIST_LABEL]
            
            features = [data[key] for key in features_key]
            data[HEATING_LOAD_LABEL], data[COLDING_LOAD_LABEL] = regressor.RegressorSingleton().predict(features)
            prediction = models.Prediction(**data)
            prediction.save()
            prediction_serializer = serializers.PredictionSerializer(prediction)
            return Response(prediction_serializer.data, status=200)
        return Response({'message': 'invalid prediction json data!'}, status=400)


class ListPredictionView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary='List Predictions with optinal filters',
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
            openapi.Parameter(name=GLAZING_AREA__DIST_LABEL, in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False),
            openapi.Parameter(name=HEATING_LOAD_LABEL, in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=False),
            openapi.Parameter(name=COLDING_LOAD_LABEL, in_=openapi.IN_QUERY, type=openapi.TYPE_NUMBER, required=False),
        ])
    def get(self, request):
        filters = {}
        query_params = request.query_params

        filter_fields = [ RELATIVE_COMPACTNESS_LABEL, SURFACE_AREA_LABEL, WALL_AREA_LABEL, ROOF_AREA_LABEL, OVERALL_HEIGHT_LABEL,
                            ORIENTATION_LABEL, GLAZING_AREA_LABEL, GLAZING_AREA__DIST_LABEL, HEATING_LOAD_LABEL, COLDING_LOAD_LABEL]

        for field in filter_fields:
            value = query_params.get(field)
            if value is not None:
                filters[field] = value

        predictions = models.Prediction.objects.filter(**filters)
        predictions_serializer = serializers.PredictionSerializer(predictions, many=True)
        predictions_list = list(predictions_serializer.data)
        return Response({'predictions': predictions_list, 'total': len(predictions_list)}, status=200)
