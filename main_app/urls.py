from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    path('contact/', views.contact_view, name='contact'),
    path('my-account/', views.my_account, name='my_account'),
    path('warranties/', views.warranty_view, name='warranties'),
    path('inspections/', views.inspections_view, name='inspections'),
    path('claims/', views.claims_view, name='claims'),
    path('claims/<int:claim_id>/edit/', views.edit_claim, name='edit_claim'),
    path('claims/<int:claim_id>/delete/', views.delete_claim, name='delete_claim'),
    path('sales-data/', views.sales_view, name='sales_data'),
    path('reporting-dashboard/', views.reporting_dashboard, name='reporting_dashboard'),
    path('sales/<int:sale_id>/add-items/', views.add_sale_items, name='add_sale_items'),
    path('sales/<int:sale_id>/delete/', views.delete_sale, name='delete_sale'),
    path('inventory/', views.inventory_view, name='inventory'),
    path('update-inventory/<int:pk>/', views.update_inventory, name='update_inventory'),
    path('inventory/<int:item_id>/update/', views.update_inventory, name='update_inventory'),
    path('inventory/<int:item_id>/delete/', views.delete_inventory, name='delete_inventory'),
    path('products/', views.products_view, name='products'),
    path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    path('about-us/', views.about_us_view, name='about-us'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)