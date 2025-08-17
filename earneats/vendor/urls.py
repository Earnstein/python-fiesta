from django.urls import path, include
from . import views


urlpatterns = [
    path("profile/", views.profileView, name="vendorProfile"),
    path("", views.httpVendorDashboard, name="vendorDashboard"),
    path("settings/", views.vendorSettings, name="vendorSettings"),
    path("menu/", include("menu.urls")),
    
    # Opening Hours CRUD
    path('opening-hours/', views.opening_hours_list, name='opening_hours_list'),
    path('opening-hours/create/', views.opening_hours_create, name='opening_hours_create'),
    path('opening-hours/edit/<int:pk>/', views.opening_hours_edit, name='opening_hours_edit'),
    path('opening-hours/delete/<int:pk>/', views.opening_hours_delete, name='opening_hours_delete'),
    path('opening-hours/bulk-edit/', views.opening_hours_bulk_edit, name='opening_hours_bulk_edit'),
]
