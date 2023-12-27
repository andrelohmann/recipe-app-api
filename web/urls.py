from django.urls import path, include
from django.views.generic import TemplateView
from . import views

app_name = 'web'

urlpatterns = [
    path('', TemplateView.as_view(template_name="web/home.html"), name="home"),
    path('privacy/', TemplateView.as_view(template_name="web/privacy.html"), name='privacy'),
    path('imprint/', TemplateView.as_view(template_name="web/imprint.html"), name='imprint'),
    path('activation/<str:uid>/<str:token>/', views.ActivationView.as_view(), name='activation'),
    # path('', RedirectView.as_view(url='catalog/', permanent=True)),
]
