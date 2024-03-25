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
    path('sales-data/', views.sales_view, name='sales_data'),
    path('sales/<int:sale_id>/add-items/', views.add_sale_items, name='add_sale_items'),
    path('sales/<int:sale_id>/delete/', views.delete_sale, name='delete_sale'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('update-inventory/<int:pk>/', views.update_inventory, name='update_inventory'),
    path('inventory/<int:item_id>/update/', views.update_inventory, name='update_inventory'),
    path('inventory/<int:item_id>/delete/', views.delete_inventory, name='delete_inventory'),
    path('products/', views.my_account, name='products'),
]
