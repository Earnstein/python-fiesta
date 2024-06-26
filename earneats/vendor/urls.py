from django.urls import path
from . import views
from accounts import views as acct_views


urlpatterns = [
    path("profile/", views.profileView, name="vendorProfile"),
    path("", acct_views.httpVendorDashboard, name="vendorDashboard"),
    path("menu/", views.menuView, name="menu"),
    path("menu/create/", views.createMenu, name="createMenu"),
    path("menu/<int:pk>/update/", views.updateMenu, name="updateMenu"),
    path("menu/<int:pk>/delete/", views.deleteMenu, name="deleteMenu"),
    path("menu/category/<int:pk>/", views.getMenuByCategory, name="getMenuByCategory"),
]
