from django.views.generic.edit import CreateView
from .forms import ContactForm
from .models import ContactRequest

class ContactCreateView(CreateView):
    model = ContactRequest
    form_class = ContactForm
    template_name = 'contact/contact_form.html'
    success_url = '/contact/success/'

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['email'] = self.request.user.email
        return initial
