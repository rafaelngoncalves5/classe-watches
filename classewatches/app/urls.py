from django.urls import path
from . import views

app_name='app'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('success', views.SuccessView.as_view(), name='success'),

    # Auth
    path('auth/signup', views.SignUpView.as_view(), name='signup'),
]