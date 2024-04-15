from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import ContactForm

# Create your views here.
class ContactCreateView(CreateView):
    template_name = 'contact/contact_form.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        return super().form_valid(form)