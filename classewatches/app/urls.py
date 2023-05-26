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

    # User and Admin
    path('user/admin', views.AdminView.as_view(), name='admin'),
    # User
    path('user/admin/update/<int:pk>', views.UpdateUserView.as_view(), name='update_user'),
    path('user/admin/delete/<int:pk>', views.DeleteUserView.as_view(), name='delete_user'),
    # Order
    path('user/admin/order/update/<slug:pk>', views.OrderUpdateView.as_view(), name='update_order'),
    path('user/admin/order/details/<slug:pk>', views.OrderDetailsView.as_view(), name='details_order'),
    path('user/admin/order/create', views.OrderCreateView.as_view(), name='create_order'),
    # Products
    path('user/admin/products/create', views.CreateProductView.as_view(), name='create_product'),
    path('user/admin/products/update/<int:pk>', views.UpdateProductView.as_view(), name='update_product'),
    path('user/admin/products/delete/<int:pk>', views.DeleteProductView.as_view(), name='delete_product'),

    # Products
    path('products', views.ProductsView.as_view(), name='products'),
    path('products/details/<int:pk>', views.ProductsDetailsView.as_view(), name='product_details'),
    
    # Cart
    path('cart/<int:pk>', views.CartView.as_view(), name='cart'),

]