from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('products/delete/<int:pk>/', views.product_delete, name='product_delete'),
    path('sales/', views.sale_list, name='sale_list'),
    path('sales/create/', views.create_sale, name='create_sale'),
    path('sales/<int:pk>/', views.sale_detail, name='sale_detail'),
    path('activity-logs/', views.activity_logs, name='activity_logs'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('export-sales/', views.export_sales_csv, name='export_sales'),
]