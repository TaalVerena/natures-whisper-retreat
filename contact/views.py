from django.views.generic.edit import CreateView
from .forms import ContactForm
from .models import ContactRequest


class ContactCreateView(CreateView):
    """A view for creating contact requests."""
    model = ContactRequest
    form_class = ContactForm
    template_name = 'contact/contact_form.html'
    success_url = '/contact/success/'

    def get_initial(self):
        """Get initial data for the contact form."""
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['email'] = self.request.user.email
        return initial
