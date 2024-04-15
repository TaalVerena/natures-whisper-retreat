from django.urls import path
from django.views.generic import TemplateView
from .views import ContactCreateView

urlpatterns = [
    path('contact/', ContactCreateView.as_view(), name='contact'),
    path('contact/success/', TemplateView.as_view(template_name='contact/success.html'), name='contact_success'),
]