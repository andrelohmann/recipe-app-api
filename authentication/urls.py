from django.urls import path, include
from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView,
)

app_name = 'authentication'

urlpatterns = [
    path('', include('djoser.urls')),
    # path('', include('djoser.urls.jwt')),
    # # override the default jwt token views
    path(
        'jwt/create/',
        CustomTokenObtainPairView.as_view(),
        name='jwt-create'
    ),
    path(
        'jwt/refresh/',
        CustomTokenRefreshView.as_view(),
        name='jwt-refresh'
    ),
    path(
        'jwt/verify/',
        CustomTokenVerifyView.as_view(),
        name='jwt-verify'
    ),
    path(
        'logout/',
        LogoutView.as_view(),
        name='logout'
    ),
]
