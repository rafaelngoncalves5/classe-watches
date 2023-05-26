from typing import Any
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, Http404
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from django import forms
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from . models import Order, Product, Cart
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import password_validation

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
        fields = ('username', 'first_name', 'last_name', 'email', 'email2',)
    
class SignUpView(generic.CreateView):
    template_name = 'app/auth/signup.html'
    model = User
    context_object_name = 'User'
    success_url = reverse_lazy('app:login')
    form_class = SignUpForm

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        print(form.cleaned_data)
        # Removing error prone data from form
        form.cleaned_data.pop('email2', None)
        form.cleaned_data.pop('password2', None)
        # Change password 1 to password to avoid key error
        password = form.cleaned_data['password1']
        form.cleaned_data.pop('password1', None)
        form.cleaned_data['password'] = password

        new_user = User.objects.create_user(**form.cleaned_data)
        new_cart = Cart.objects.create(user=new_user)
        return redirect('app:success')

class LoginView(LoginView):
    template_name = 'app/auth/login.html'
    next_page = reverse_lazy('app:success')

class LogoutView(LogoutView):
    next_page = reverse_lazy('app:success')

# User
class SuperUserRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self) -> bool | None:
        return self.request.user.is_superuser

class AdminView(SuperUserRequiredMixin, generic.TemplateView):
    template_name = 'app/admin/index.html'
    login_url = reverse_lazy('app:login')

    def get_context_data(self, **kwargs):
        context = {
            'Order': Order.objects.all().order_by('-order_date'),
            'Product': Product.objects.all().order_by('quantity'),
            'User': User.objects.all(),
        }

        return context
    
class UserView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('app:login')
    template_name = 'app/user/index.html'

    def get_context_data(self, **kwargs):
        context = {
            'User': self.request.user,
            'Orders': Order.objects.filter(cart=self.request.user.cart).order_by('-order_date')[:5]
        }
        return context
    
# Products
class ProductForm(forms.ModelForm):
    quantity = forms.IntegerField(label="Quantidade", min_value=1, initial=1)
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'quantity', 'image_cover', 'image2', 'image3']

class CreateProductView(SuperUserRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('app:login')
    template_name = 'app/admin/products/create.html'
    success_url = reverse_lazy('app:success')
    form_class = ProductForm

class UpdateProductView(SuperUserRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('app:login')
    template_name = 'app/admin/products/create.html'
    success_url = reverse_lazy('app:success')
    form_class = ProductForm
    model = Product

class DeleteProductView(SuperUserRequiredMixin, generic.DeleteView):
    login_url = reverse_lazy('app:login')
    model = Product
    success_url = reverse_lazy('app:success')

# Users
class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'is_superuser',)

class UpdateUserView(SuperUserRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('app:login')
    model = User
    success_url = reverse_lazy('app:success')
    form_class = UpdateUserForm
    template_name = 'app/admin/user/update.html'

class DeleteUserView(SuperUserRequiredMixin, generic.DeleteView):
    login_url = reverse_lazy('app:login')
    model = User
    success_url = reverse_lazy('app:success')

# Orders
class OrderCreateView(SuperUserRequiredMixin, generic.CreateView):
    login_url = reverse_lazy('app:login')
    model = Order
    success_url = reverse_lazy('app:success')
    template_name = 'app/admin/order/create.html'
    fields = ['id', 'cart', 'products', 'total', 'order_date', 'phone_number', 'phone_number2', 'state', 'district', 'street', 'street_number', 'complement', 'cep', 'status', 'tracking_link']

class OrderUpdateView(SuperUserRequiredMixin, generic.UpdateView):
    login_url = reverse_lazy('app:login')
    model = Order
    success_url = reverse_lazy('app:success')
    template_name = 'app/admin/order/update.html'
    fields = ['status', 'tracking_link']

class OrderDetailsView(SuperUserRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('app:login')
    template_name = 'app/admin/order/details.html'
    model = Order
    context_object_name = 'Order'

# Products 2
class ProductsView(generic.ListView):
    queryset = Product.objects.all().order_by('-price')
    context_object_name = 'Product'
    template_name = 'app/products/index.html'

class ProductsDetailsView(generic.DetailView):
    model = Product
    context_object_name = 'Product'
    template_name = 'app/products/details.html'

# Cart
class CartView(LoginRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('app:login')
    template_name = 'app/cart/index.html'
    model = Cart
    context_object_name = 'Cart'

def add_to_cart(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # 1 - Grabs the cart
            cart: Cart = get_object_or_404(Cart, pk=request.user.cart.id)
            # 2 - Grabs a product id, via query param
            product = Product.objects.get(pk=id)
            # 3 - Adds the cart using related objects
            product.cart.add(cart)
            
            return redirect('app:cart', cart.id)
    return redirect('app:login')

def remove_from_cart(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # 1 - Grabs the cart
            cart: Cart = get_object_or_404(Cart, pk=request.user.cart.id)
            # 2 - Grabs a product id, via query param
            product = Product.objects.get(pk=id)
            # 3 - Removes the cart using related objects
            product.cart.remove(cart)
            
            return redirect('app:cart', cart.id)
    return redirect('app:login')

# Shipping
class ShippingView(LoginRequiredMixin, generic.TemplateView):
    login_url = reverse_lazy('app:login')
    template_name = 'app/payment/shipping.html'