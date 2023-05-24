from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.views import LoginView, LogoutView

# Validators
from django.core.exceptions import ValidationError

# Create your views here.
class IndexView(generic.TemplateView):
    template_name = 'app/index.html'

class SuccessView(generic.TemplateView):
    template_name = 'success.html'

# Auth
class SignUpForm(UserCreationForm):

    email = forms.EmailField(required=True, widget=forms.EmailInput(), label="Endereço de email:")
    email2 = forms.EmailField(required=True, widget=forms.EmailInput(), label='Confirmação de email:', help_text='Informe o mesmo email informado anteriormente, para verificação.')

    def clean(self):
        form_data = self.cleaned_data
        email_exists = User.objects.filter(email=form_data['email']).exists()

        if form_data['email'] == form_data['email2'] and not email_exists:
            return form_data
        elif not form_data['email'] == form_data['email2']:
            raise ValidationError("Emails não são iguais.")
        elif email_exists:
            raise ValidationError("Email já cadastrado.")

    class Meta(UserCreationForm.Meta):
        fields = ('first_name', 'last_name', 'email', 'email2',)
    
class SignUpView(generic.CreateView):
    template_name = 'app/auth/signup.html'
    model = User
    context_object_name = 'User'
    success_url = reverse_lazy('app:success')
    form_class = SignUpForm

class LoginView(LoginView):
    template_name = 'app/auth/login.html'
    success_url = reverse_lazy('app:success')