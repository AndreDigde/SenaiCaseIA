from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .constants import PREDICTION_ID_LABEL

from . import views

urlpatterns = [
    path('auth/', views.AuthView.as_view(), name='auth_user'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path(f'prediction/<int:{PREDICTION_ID_LABEL}>', views.PredictionView.as_view(), name='get_prediction'),
    path('prediction', views.PerformPredictionView.as_view(), name='post_prediction'),
    path('predictions', views.ListPredictionView.as_view(), name='predictions'),
]
