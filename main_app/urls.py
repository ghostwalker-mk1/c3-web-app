from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('contact/', views.contact_view, name='contact'),
    path('my-account/', views.my_account, name='my_account'),
    path('warranty/', views.my_account, name='warranty'),
    path('inspections/', views.my_account, name='inspections'),
    path('claims/', views.my_account, name='claims'),
    path('reporting/', views.my_account, name='reporting'),
    path('inventory/', views.my_account, name='inventory'),
    path('products/', views.my_account, name='products'),
]
