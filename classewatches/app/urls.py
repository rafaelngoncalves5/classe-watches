from django.urls import path
from . import views

app_name='app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('success', views.SuccessView.as_view(), name='success'),

    # Auth
    path('auth/signup', views.SignUpView.as_view(), name='signup'),
    path('auth/login', views.LoginView.as_view(), name='login'),
    path('auth/logout', views.LogoutView.as_view(), name='logout'),

    # User
    path('user/admin', views.AdminView.as_view(), name='admin'),

    # Products
    path('user/admin/products/create', views.CreateProduct.as_view(), name='create_product'),
    
]