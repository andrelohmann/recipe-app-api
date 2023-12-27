from django.views.generic import TemplateView

# Create your views here.
class ActivationView(TemplateView):
    template_name="web/activation.html"